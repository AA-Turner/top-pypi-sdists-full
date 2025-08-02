r'''
# Amazon EventBridge Pipes Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

EventBridge Pipes let you create source to target connections between several
AWS services. While transporting messages from a source to a target the messages
can be filtered, transformed and enriched.

![diagram of pipes](https://d1.awsstatic.com/product-marketing/EventBridge/Product-Page-Diagram_Amazon-EventBridge-Pipes.cd7961854be4432d63f6158ffd18271d6c9fa3ec.png)

For more details see the [service documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html).

## Pipe

[EventBridge Pipes](https://aws.amazon.com/blogs/aws/new-create-point-to-point-integrations-between-event-producers-and-consumers-with-amazon-eventbridge-pipes/)
is a fully managed service that enables point-to-point integrations between
event producers and consumers. Pipes can be used to connect several AWS services
to each other, or to connect AWS services to external services.

A pipe has a source and a target. The source events can be filtered and enriched
before reaching the target.

## Example - pipe usage

> The following code examples use an example implementation of a [source](#source) and [target](#target).

To define a pipe you need to create a new `Pipe` construct. The `Pipe` construct needs a source and a target.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue)
)
```

This minimal example creates a pipe with a SQS queue as source and a SQS queue as target.
Messages from the source are put into the body of the target message.

## Source

A source is a AWS Service that is polled. The following sources are possible:

* [Amazon DynamoDB stream](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html)
* [Amazon Kinesis stream](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kinesis.html)
* [Amazon MQ broker](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-mq.html)
* [Amazon MSK stream](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-msk.html)
* [Amazon SQS queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-sqs.html)
* [Apache Kafka stream](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kafka.html)

Currently, DynamoDB, Kinesis, and SQS are supported. If you are interested in support for additional sources,
kindly let us know by opening a GitHub issue or raising a PR.

### Example source

```python
# source_queue: sqs.Queue

pipe_source = SqsSource(source_queue)
```

## Filter

A filter can be used to filter the events from the source before they are
forwarded to the enrichment or, if no enrichment is present, target step. Multiple filter expressions are possible.
If one of the filter expressions matches, the event is forwarded to the enrichment or target step.

### Example - filter usage

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


source_filter = pipes.Filter([
    pipes.FilterPattern.from_object({
        "body": {
            # only forward events with customerType B2B or B2C
            "customer_type": ["B2B", "B2C"]
        }
    })
])

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue),
    filter=source_filter
)
```

This example shows a filter that only forwards events with the `customerType` B2B or B2C from the source messages. Messages that are not matching the filter are not forwarded to the enrichment or target step.

You can define multiple filter pattern which are combined with a logical `OR`.

Additional filter pattern and details can be found in the EventBridge pipes [docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-filtering.html).

## Input transformation

For enrichments and targets the input event can be transformed. The transformation is applied for each item of the batch.
A transformation has access to the input event as well to some context information of the pipe itself like the name of the pipe.
See [docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-input-transformation.html) for details.

### Example - input transformation from object

The input transformation can be created from an object. The object can contain static values, dynamic values or pipe variables.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


target_input_transformation = pipes.InputTransformation.from_object({
    "static_field": "static value",
    "dynamic_field": pipes.DynamicInput.from_event_path("$.body.payload"),
    "pipe_variable": pipes.DynamicInput.pipe_name
})

pipe = pipes.Pipe(self, "Pipe",
    pipe_name="MyPipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue,
        input_transformation=target_input_transformation
    )
)
```

This example shows a transformation that adds a static field, a dynamic field and a pipe variable to the input event. The dynamic field is extracted from the input event. The pipe variable is extracted from the pipe context.

So when the following batch of input events is processed by the pipe

```json
[
  {
    ...
    "body": "{\"payload\": \"Test message.\"}",
    ...
  }
]
```

it is converted into the following payload:

```json
[
  {
    ...
    "staticField": "static value",
    "dynamicField": "Test message.",
    "pipeVariable": "MyPipe",
    ...
  }
]
```

If the transformation is applied to a target it might be converted to a string representation. For example, the resulting SQS message body looks like this:

```json
[
  {
    ...
    "body": "{\"staticField\": \"static value\", \"dynamicField\": \"Test message.\", \"pipeVariable\": \"MyPipe\"}",
    ...
  }
]
```

### Example - input transformation from event path

In cases where you want to forward only a part of the event to the target you can use the transformation event path.

> This only works for targets because the enrichment needs to have a valid json as input.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


target_input_transformation = pipes.InputTransformation.from_event_path("$.body.payload")

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue,
        input_transformation=target_input_transformation
    )
)
```

This transformation extracts the body of the event.

So when the following batch of input events is processed by the pipe

```json
 [
  {
    ...
    "body": "\"{\"payload\": \"Test message.\"}\"",
    ...
  }
]
```

it is converted into the following target payload:

```json
[
  {
    ...
    "body": "Test message."
    ...
  }
]
```

> The [implicit payload parsing](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-input-transformation.html#input-transform-implicit) (e.g. SQS message body to JSON) only works if the input is the source payload. Implicit body parsing is not applied on enrichment results.

### Example - input transformation from text

In cases where you want to forward a static text to the target or use your own formatted `inputTemplate` you can use the transformation from text.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


target_input_transformation = pipes.InputTransformation.from_text("My static text")

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue,
        input_transformation=target_input_transformation
    )
)
```

This transformation forwards the static text to the target.

```json
[
  {
    ...
    "body": "My static text"
    ...
  }
]
```

## Enrichment

In the enrichment step the (un)filtered payloads from the source can be used to invoke one of the following services:

* API destination
* Amazon API Gateway
* Lambda function
* Step Functions state machine

  * only express workflow

### Example enrichment implementation

> Currently no implementation exist for any of the supported enrichments. The following example shows how an implementation can look like. The actual implementation is not part of this package and will be in a separate one.

```python
@jsii.implements(pipes.IEnrichment)
class LambdaEnrichment:

    def __init__(self, lambda_, props=None):
        self.enrichment_arn = lambda_.function_arn
        self.input_transformation = props.input_transformation

    def bind(self, pipe):
        return pipes.EnrichmentParametersConfig(
            enrichment_parameters=cdk.aws_pipes.CfnPipe.PipeEnrichmentParametersProperty(
                input_template=self.input_transformation.bind(pipe).input_template
            )
        )

    def grant_invoke(self, pipe_role):
        self.lambda_.grant_invoke(pipe_role)
```

An enrichment implementation needs to provide the `enrichmentArn`, `enrichmentParameters` and grant the pipe role invoke access to the enrichment.

### Example - enrichment usage

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue
# enrichment_lambda: lambda.Function


enrichment_input_transformation = pipes.InputTransformation.from_object({
    "static_field": "static value",
    "dynamic_field": pipes.DynamicInput.from_event_path("$.body.payload"),
    "pipe_variable": pipes.DynamicInput.pipe_name
})

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue),
    enrichment=LambdaEnrichment(enrichment_lambda, {
        "input_transformation": enrichment_input_transformation
    })
)
```

This example adds a lambda function as enrichment to the pipe. The lambda function is invoked with the batch of messages from the source after applying the transformation. The lambda function can return a result which is forwarded to the target.

So the following batch of input events is processed by the pipe

```json
[
  {
    ...
    "body": "{\"payload\": \"Test message.\"}",
    ...
  }
]
```

it is converted into the following payload which is sent to the lambda function.

```json
[
  {
    ...
    "staticField": "static value",
    "dynamicField": "Test message.",
    "pipeVariable": "MyPipe",
    ...
  }
]
```

The lambda function can return a result which is forwarded to the target.
For example a lambda function that returns a concatenation of the static field, dynamic field and pipe variable

```python
def handler(event):
    return event.static_field + "-" + event.dynamic_field + "-" + event.pipe_variable
```

will produce the following target message in the target SQS queue.

```json
[
  {
    ...
    "body": "static value-Test message.-MyPipe",
    ...
  }
]
```

## Target

A Target is the end of the Pipe. After the payload from the source is pulled,
filtered and enriched it is forwarded to the target. For now the following
targets are supported:

* [API destination](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-api-destinations.html)
* [API Gateway](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-api-gateway-target.html)
* [Batch job queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html#pipes-targets-specifics-batch)
* [CloudWatch log group](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html#pipes-targets-specifics-cwl)
* [ECS task](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html#pipes-targets-specifics-ecs-task)
* Event bus in the same account and Region
* Firehose delivery stream
* Inspector assessment template
* Kinesis stream
* Lambda function (SYNC or ASYNC)
* Redshift cluster data API queries
* SageMaker Pipeline
* SNS topic
* SQS queue
* Step Functions state machine

  * Express workflows (ASYNC)
  * Standard workflows (SYNC or ASYNC)

The target event can be transformed before it is forwarded to the target using
the same input transformation as in the enrichment step.

### Example target

```python
# target_queue: sqs.Queue

pipe_target = SqsTarget(target_queue)
```

## Log destination

A pipe can produce log events that are forwarded to different log destinations.
You can configure multiple destinations, but all the destination share the same log level and log data.
For details check the official [documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html).

The log level and data that is included in the log events is configured on the pipe class itself.
The actual destination is defined independently, and there are three options:

1. `CloudwatchLogsLogDestination`
2. `FirehoseLogDestination`
3. `S3LogDestination`

### Example log destination usage

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue
# log_group: logs.LogGroup


cwl_log_destination = pipes.CloudwatchLogsLogDestination(log_group)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue),
    log_level=pipes.LogLevel.TRACE,
    log_include_execution_data=[pipes.IncludeExecutionData.ALL],
    log_destinations=[cwl_log_destination]
)
```

This example uses a CloudWatch Logs log group to store the log emitted during a pipe execution.
The log level is set to `TRACE` so all steps of the pipe are logged.
Additionally all execution data is logged as well.

## Encrypt pipe data with KMS

You can specify that EventBridge use a customer managed key to encrypt pipe data stored at rest,
rather than use an AWS owned key as is the default.
Details can be found in the [documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-encryption-pipes-cmkey.html).

To do this, you need to specify the key in the `kmsKey` property of the pipe.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue
# kms_key: kms.Key


pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=SqsTarget(target_queue),
    kms_key=kms_key,
    # pipeName is required when using a KMS key
    pipe_name="MyPipe"
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_pipes as _aws_cdk_aws_pipes_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-alpha.DesiredState")
class DesiredState(enum.Enum):
    '''(experimental) The state the pipe should be in.

    :stability: experimental
    '''

    RUNNING = "RUNNING"
    '''(experimental) The pipe should be running.

    :stability: experimental
    '''
    STOPPED = "STOPPED"
    '''(experimental) The pipe should be stopped.

    :stability: experimental
    '''


@jsii.implements(_aws_cdk_ceddda9d.IResolvable)
class DynamicInput(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.DynamicInput",
):
    '''(experimental) Dynamic variables that can be used in the input transformation.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        
        
        target_input_transformation = pipes.InputTransformation.from_object({
            "static_field": "static value",
            "dynamic_field": pipes.DynamicInput.from_event_path("$.body.payload"),
            "pipe_variable": pipes.DynamicInput.pipe_name
        })
        
        pipe = pipes.Pipe(self, "Pipe",
            pipe_name="MyPipe",
            source=SqsSource(source_queue),
            target=SqsTarget(target_queue,
                input_transformation=target_input_transformation
            )
        )
    '''

    @jsii.member(jsii_name="fromEventPath")
    @builtins.classmethod
    def from_event_path(cls, path: builtins.str) -> "DynamicInput":
        '''(experimental) Value from the event payload at jsonPath.

        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5bbb77d96c2570787e5e35a986888ea8bb0bc2ddd772916e47d846e4af16c2)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("DynamicInput", jsii.sinvoke(cls, "fromEventPath", [path]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: _aws_cdk_ceddda9d.IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860e63dc447cbad7fc641786dc20a0b496495e9b8a1a5bfe862a8b2ed5672a0d)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        '''(experimental) Return a JSON representation of a dynamic input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of a dynamic input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="enrichmentArn")
    def enrichment_arn(cls) -> "DynamicInput":
        '''(experimental) The ARN of the enrichment of the pipe.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "enrichmentArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="event")
    def event(cls) -> "DynamicInput":
        '''(experimental) The event as received by the input transformer.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "event"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="eventIngestionTime")
    def event_ingestion_time(cls) -> "DynamicInput":
        '''(experimental) The time at which the event was received by the input transformer.

        This is an ISO 8601 timestamp. This time is different for the enrichment input transformer and the target input transformer, depending on when the enrichment completed processing the event.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "eventIngestionTime"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="eventJson")
    def event_json(cls) -> "DynamicInput":
        '''(experimental) The same as aws.pipes.event, but the variable only has a value if the original payload, either from the source or returned by the enrichment, is JSON. If the pipe has an encoded field, such as the Amazon SQS body field or the Kinesis data, those fields are decoded and turned into valid JSON. Because it isn't escaped, the variable can only be used as a value for a JSON field. For more information, see Implicit body data parsing.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "eventJson"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="pipeArn")
    def pipe_arn(cls) -> "DynamicInput":
        '''(experimental) The Amazon Resource Name (ARN) of the pipe.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "pipeArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="pipeName")
    def pipe_name(cls) -> "DynamicInput":
        '''(experimental) The name of the pipe.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "pipeName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="sourceArn")
    def source_arn(cls) -> "DynamicInput":
        '''(experimental) The ARN of the event source of the pipe.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "sourceArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="targetArn")
    def target_arn(cls) -> "DynamicInput":
        '''(experimental) The ARN of the target of the pipe.

        :stability: experimental
        '''
        return typing.cast("DynamicInput", jsii.sget(cls, "targetArn"))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        This may return an array with a single informational element indicating how
        to get this property populated, if it was skipped for performance reasons.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="displayHint")
    def display_hint(self) -> builtins.str:
        '''(experimental) Human readable display hint about the event pattern.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayHint"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.EnrichmentParametersConfig",
    jsii_struct_bases=[],
    name_mapping={"enrichment_parameters": "enrichmentParameters"},
)
class EnrichmentParametersConfig:
    def __init__(
        self,
        *,
        enrichment_parameters: typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeEnrichmentParametersProperty, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) The parameters required to set up enrichment on your pipe.

        :param enrichment_parameters: (experimental) The parameters for the enrichment target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmentparameters.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            
            enrichment_parameters_config = pipes_alpha.EnrichmentParametersConfig(
                enrichment_parameters=PipeEnrichmentParametersProperty(
                    http_parameters=PipeEnrichmentHttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input_template="inputTemplate"
                )
            )
        '''
        if isinstance(enrichment_parameters, dict):
            enrichment_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeEnrichmentParametersProperty(**enrichment_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be50f45da4d8fc1e4aa1b783ed4d3d35da416296c1f3527ebe16e9c865a00a1f)
            check_type(argname="argument enrichment_parameters", value=enrichment_parameters, expected_type=type_hints["enrichment_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enrichment_parameters": enrichment_parameters,
        }

    @builtins.property
    def enrichment_parameters(
        self,
    ) -> _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeEnrichmentParametersProperty:
        '''(experimental) The parameters for the enrichment target.

        :stability: experimental
        '''
        result = self._values.get("enrichment_parameters")
        assert result is not None, "Required property 'enrichment_parameters' is missing"
        return typing.cast(_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeEnrichmentParametersProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnrichmentParametersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilterPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.FilterPattern",
):
    '''(experimental) Generate a filter pattern from an input.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        
        
        source_filter = pipes.Filter([
            pipes.FilterPattern.from_object({
                "body": {
                    # only forward events with customerType B2B or B2C
                    "customer_type": ["B2B", "B2C"]
                }
            })
        ])
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=SqsTarget(target_queue),
            filter=source_filter
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(
        cls,
        pattern_object: typing.Mapping[builtins.str, typing.Any],
    ) -> "IFilterPattern":
        '''(experimental) Generates a filter pattern from a JSON object.

        :param pattern_object: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bd3fb3b0ffe9a4d7e3fe32ab50edde2c475b6ce11cad8df1ada38d5e3ad115)
            check_type(argname="argument pattern_object", value=pattern_object, expected_type=type_hints["pattern_object"])
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "fromObject", [pattern_object]))


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.IEnrichment")
class IEnrichment(typing_extensions.Protocol):
    '''(experimental) Enrichment step to enhance the data from the source before sending it to the target.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enrichmentArn")
    def enrichment_arn(self) -> builtins.str:
        '''(experimental) The ARN of the enrichment resource.

        Length Constraints: Minimum length of 0. Maximum length of 1600.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-enrichment
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: "IPipe") -> EnrichmentParametersConfig:
        '''(experimental) Bind this enrichment to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipes role to invoke the enrichment.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IEnrichmentProxy:
    '''(experimental) Enrichment step to enhance the data from the source before sending it to the target.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.IEnrichment"

    @builtins.property
    @jsii.member(jsii_name="enrichmentArn")
    def enrichment_arn(self) -> builtins.str:
        '''(experimental) The ARN of the enrichment resource.

        Length Constraints: Minimum length of 0. Maximum length of 1600.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-enrichment
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "enrichmentArn"))

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: "IPipe") -> EnrichmentParametersConfig:
        '''(experimental) Bind this enrichment to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc5492815137155b1832922d330923c5324c2144c6b7ce6f629cc5e40f4a455)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(EnrichmentParametersConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipes role to invoke the enrichment.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1ad4c7fe348a9788b14ee41d1c66c13826fc937049e66fdf554ed83bfe7baf)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantInvoke", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEnrichment).__jsii_proxy_class__ = lambda : _IEnrichmentProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.IFilter")
class IFilter(typing_extensions.Protocol):
    '''(experimental) The collection of event patterns used to filter events.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.List["IFilterPattern"]:
        '''(experimental) Filters for the source.

        :stability: experimental
        '''
        ...

    @filters.setter
    def filters(self, value: typing.List["IFilterPattern"]) -> None:
        ...


class _IFilterProxy:
    '''(experimental) The collection of event patterns used to filter events.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.IFilter"

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.List["IFilterPattern"]:
        '''(experimental) Filters for the source.

        :stability: experimental
        '''
        return typing.cast(typing.List["IFilterPattern"], jsii.get(self, "filters"))

    @filters.setter
    def filters(self, value: typing.List["IFilterPattern"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d300fa623a25928741c7906df5849b8fe94e2c857016ddc27c9bfa606840c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilter).__jsii_proxy_class__ = lambda : _IFilterProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.IFilterPattern")
class IFilterPattern(typing_extensions.Protocol):
    '''(experimental) Filter events using an event pattern.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-filtering.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        '''(experimental) Stringified version of the filter pattern.

        :stability: experimental
        '''
        ...

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        ...


class _IFilterPatternProxy:
    '''(experimental) Filter events using an event pattern.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-filtering.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.IFilterPattern"

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        '''(experimental) Stringified version of the filter pattern.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c692a10525cf42d6819fccf1ba8a1c1a5e2c95948fc2df661221cdb6a2669568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilterPattern).__jsii_proxy_class__ = lambda : _IFilterPatternProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.IInputTransformation")
class IInputTransformation(typing_extensions.Protocol):
    '''(experimental) Transform or replace the input event payload.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: "IPipe") -> "InputTransformationConfig":
        '''(experimental) Bind the input transformation to the pipe and returns the inputTemplate string.

        :param pipe: -

        :stability: experimental
        '''
        ...


class _IInputTransformationProxy:
    '''(experimental) Transform or replace the input event payload.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.IInputTransformation"

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: "IPipe") -> "InputTransformationConfig":
        '''(experimental) Bind the input transformation to the pipe and returns the inputTemplate string.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c56b2ae871eaf486f0abeb0df58eb5ca1718e69de303cf680b518c5b755040)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast("InputTransformationConfig", jsii.invoke(self, "bind", [pipe]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInputTransformation).__jsii_proxy_class__ = lambda : _IInputTransformationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.ILogDestination")
class ILogDestination(typing_extensions.Protocol):
    '''(experimental) Log destination base class.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: "IPipe") -> "LogDestinationConfig":
        '''(experimental) Bind the log destination to the pipe.

        :param pipe: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the log destination.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _ILogDestinationProxy:
    '''(experimental) Log destination base class.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.ILogDestination"

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: "IPipe") -> "LogDestinationConfig":
        '''(experimental) Bind the log destination to the pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fc07eda1cf81cdd6181b1c56681e9296a86e8c0e3831080bff1759881ddb5c)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast("LogDestinationConfig", jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the log destination.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e82ee136087b77e6440c7ba18e27a104e108c7b4e2fdc3b9347dc967f7e550)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogDestination).__jsii_proxy_class__ = lambda : _ILogDestinationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.IPipe")
class IPipe(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Interface representing a created or an imported ``Pipe``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="pipeArn")
    def pipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the pipe.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#Arn-fn::getatt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="pipeName")
    def pipe_name(self) -> builtins.str:
        '''(experimental) The name of the pipe.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-name
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="pipeRole")
    def pipe_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by the pipe.

        For imported pipes it assumes that the default role is used.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPipeProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Interface representing a created or an imported ``Pipe``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.IPipe"

    @builtins.property
    @jsii.member(jsii_name="pipeArn")
    def pipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the pipe.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#Arn-fn::getatt
        '''
        return typing.cast(builtins.str, jsii.get(self, "pipeArn"))

    @builtins.property
    @jsii.member(jsii_name="pipeName")
    def pipe_name(self) -> builtins.str:
        '''(experimental) The name of the pipe.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "pipeName"))

    @builtins.property
    @jsii.member(jsii_name="pipeRole")
    def pipe_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by the pipe.

        For imported pipes it assumes that the default role is used.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "pipeRole"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPipe).__jsii_proxy_class__ = lambda : _IPipeProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.ISource")
class ISource(typing_extensions.Protocol):
    '''(experimental) Source interface.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''(experimental) The ARN of the source resource.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: IPipe) -> "SourceConfig":
        '''(experimental) Bind the source to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _ISourceProxy:
    '''(experimental) Source interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.ISource"

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''(experimental) The ARN of the source resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: IPipe) -> "SourceConfig":
        '''(experimental) Bind the source to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc51442e0b59cd40f4211e4205ed3feaa6ab35fd337c948849a7fc75d273bea)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b7f3713c7dd058bbfa6fd41eff30b60ed5cd0026f7f24037edc7503d1d833c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISource).__jsii_proxy_class__ = lambda : _ISourceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-pipes-alpha.ITarget")
class ITarget(typing_extensions.Protocol):
    '''(experimental) Target configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: IPipe) -> "TargetConfig":
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _ITargetProxy:
    '''(experimental) Target configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-pipes-alpha.ITarget"

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: IPipe) -> "TargetConfig":
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e93dc435b6334c19ccf66163b6aad3d46712c8f63afc72a3d5267c12e8335b)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast("TargetConfig", jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cc64b1eb25062d3fcee449052e46d0ae2ef8f2a0ee990643ee2c9cbfb79aa1)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITarget).__jsii_proxy_class__ = lambda : _ITargetProxy


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-alpha.IncludeExecutionData")
class IncludeExecutionData(enum.Enum):
    '''(experimental) Log data configuration for a pipe.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        # log_group: logs.LogGroup
        
        
        cwl_log_destination = pipes.CloudwatchLogsLogDestination(log_group)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=SqsTarget(target_queue),
            log_level=pipes.LogLevel.TRACE,
            log_include_execution_data=[pipes.IncludeExecutionData.ALL],
            log_destinations=[cwl_log_destination]
        )
    '''

    ALL = "ALL"
    '''(experimental) Specify ALL to include the execution data (specifically, the payload, awsRequest, and awsResponse fields) in the log messages for this pipe.

    :stability: experimental
    '''


@jsii.implements(IInputTransformation)
class InputTransformation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.InputTransformation",
):
    '''(experimental) Transform or replace the input event payload.

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

    @jsii.member(jsii_name="fromEventPath")
    @builtins.classmethod
    def from_event_path(
        cls,
        json_path_expression: builtins.str,
    ) -> "InputTransformation":
        '''(experimental) Creates an InputTransformation from a jsonPath expression of the input event.

        :param json_path_expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182c04a131444303df0e217e3900a484fbc6ca8845dd17981187d035c3aa3054)
            check_type(argname="argument json_path_expression", value=json_path_expression, expected_type=type_hints["json_path_expression"])
        return typing.cast("InputTransformation", jsii.sinvoke(cls, "fromEventPath", [json_path_expression]))

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(
        cls,
        input_template: typing.Mapping[builtins.str, typing.Any],
    ) -> "InputTransformation":
        '''(experimental) Creates an InputTransformation from a pipe variable.

        :param input_template: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2bb77e9adef2b6e1b25daac546880929aa3cc34ea9887fe45d38161dc8a805)
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
        return typing.cast("InputTransformation", jsii.sinvoke(cls, "fromObject", [input_template]))

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, input_template: builtins.str) -> "InputTransformation":
        '''(experimental) Creates an InputTransformation from a string.

        :param input_template: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fa91b1b3adb6b7383532aa0abf70cabcdfb70451cff3e408cb68ce7373f99d)
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
        return typing.cast("InputTransformation", jsii.sinvoke(cls, "fromText", [input_template]))

    @jsii.member(jsii_name="bind")
    def bind(self, pipe: IPipe) -> "InputTransformationConfig":
        '''(experimental) Bind the input transformation to the pipe and returns the inputTemplate string.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9928c7373e9e39af7fd3151eb77ece0c9a46ed64f6c611d61ea7d11d51c02213)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast("InputTransformationConfig", jsii.invoke(self, "bind", [pipe]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.InputTransformationConfig",
    jsii_struct_bases=[],
    name_mapping={"input_template": "inputTemplate"},
)
class InputTransformationConfig:
    def __init__(self, *, input_template: builtins.str) -> None:
        '''(experimental) The inputTemplate that is used to transform the input event payload with unquoted variables.

        :param input_template: (experimental) The inputTemplate that is used to transform the input event payload.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            
            input_transformation_config = pipes_alpha.InputTransformationConfig(
                input_template="inputTemplate"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630bec5abec8acb015b6dae32bfdea83eebf4822e821d1d788f9f55a4d3283c1)
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_template": input_template,
        }

    @builtins.property
    def input_template(self) -> builtins.str:
        '''(experimental) The inputTemplate that is used to transform the input event payload.

        :stability: experimental
        '''
        result = self._values.get("input_template")
        assert result is not None, "Required property 'input_template' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InputTransformationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.LogDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters"},
)
class LogDestinationConfig:
    def __init__(
        self,
        *,
        parameters: typing.Union["LogDestinationParameters", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Log destination configuration.

        :param parameters: (experimental) Get the log destination configuration parameters.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            
            log_destination_config = pipes_alpha.LogDestinationConfig(
                parameters=pipes_alpha.LogDestinationParameters(
                    cloudwatch_logs_log_destination=CloudwatchLogsLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    firehose_log_destination=FirehoseLogDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn"
                    ),
                    s3_log_destination=S3LogDestinationProperty(
                        bucket_name="bucketName",
                        bucket_owner="bucketOwner",
                        output_format="outputFormat",
                        prefix="prefix"
                    )
                )
            )
        '''
        if isinstance(parameters, dict):
            parameters = LogDestinationParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c221263227417f49ed8ca8afd4f2ca6238bec626c6b82c6ad0384b5e9cca219)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameters": parameters,
        }

    @builtins.property
    def parameters(self) -> "LogDestinationParameters":
        '''(experimental) Get the log destination configuration parameters.

        :stability: experimental
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast("LogDestinationParameters", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.LogDestinationParameters",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_logs_log_destination": "cloudwatchLogsLogDestination",
        "firehose_log_destination": "firehoseLogDestination",
        "s3_log_destination": "s3LogDestination",
    },
)
class LogDestinationParameters:
    def __init__(
        self,
        *,
        cloudwatch_logs_log_destination: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.CloudwatchLogsLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        firehose_log_destination: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.FirehoseLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_log_destination: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.S3LogDestinationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Log destination configuration parameters.

        :param cloudwatch_logs_log_destination: (experimental) The logging configuration settings for the pipe. Default: - none
        :param firehose_log_destination: (experimental) The Amazon Data Firehose logging configuration settings for the pipe. Default: - none
        :param s3_log_destination: (experimental) The Amazon S3 logging configuration settings for the pipe. Default: - none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            
            log_destination_parameters = pipes_alpha.LogDestinationParameters(
                cloudwatch_logs_log_destination=CloudwatchLogsLogDestinationProperty(
                    log_group_arn="logGroupArn"
                ),
                firehose_log_destination=FirehoseLogDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn"
                ),
                s3_log_destination=S3LogDestinationProperty(
                    bucket_name="bucketName",
                    bucket_owner="bucketOwner",
                    output_format="outputFormat",
                    prefix="prefix"
                )
            )
        '''
        if isinstance(cloudwatch_logs_log_destination, dict):
            cloudwatch_logs_log_destination = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.CloudwatchLogsLogDestinationProperty(**cloudwatch_logs_log_destination)
        if isinstance(firehose_log_destination, dict):
            firehose_log_destination = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.FirehoseLogDestinationProperty(**firehose_log_destination)
        if isinstance(s3_log_destination, dict):
            s3_log_destination = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.S3LogDestinationProperty(**s3_log_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e011cd2ae75207e0b7e6eec35a33b026d9aa2fefab7715f3111f5d14739cc3)
            check_type(argname="argument cloudwatch_logs_log_destination", value=cloudwatch_logs_log_destination, expected_type=type_hints["cloudwatch_logs_log_destination"])
            check_type(argname="argument firehose_log_destination", value=firehose_log_destination, expected_type=type_hints["firehose_log_destination"])
            check_type(argname="argument s3_log_destination", value=s3_log_destination, expected_type=type_hints["s3_log_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_logs_log_destination is not None:
            self._values["cloudwatch_logs_log_destination"] = cloudwatch_logs_log_destination
        if firehose_log_destination is not None:
            self._values["firehose_log_destination"] = firehose_log_destination
        if s3_log_destination is not None:
            self._values["s3_log_destination"] = s3_log_destination

    @builtins.property
    def cloudwatch_logs_log_destination(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.CloudwatchLogsLogDestinationProperty]:
        '''(experimental) The logging configuration settings for the pipe.

        :default: - none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-cloudwatchlogslogdestination
        :stability: experimental
        '''
        result = self._values.get("cloudwatch_logs_log_destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.CloudwatchLogsLogDestinationProperty], result)

    @builtins.property
    def firehose_log_destination(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.FirehoseLogDestinationProperty]:
        '''(experimental) The Amazon Data Firehose logging configuration settings for the pipe.

        :default: - none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-firehoselogdestination
        :stability: experimental
        '''
        result = self._values.get("firehose_log_destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.FirehoseLogDestinationProperty], result)

    @builtins.property
    def s3_log_destination(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.S3LogDestinationProperty]:
        '''(experimental) The Amazon S3 logging configuration settings for the pipe.

        :default: - none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-s3logdestination
        :stability: experimental
        '''
        result = self._values.get("s3_log_destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.S3LogDestinationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogDestinationParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-alpha.LogLevel")
class LogLevel(enum.Enum):
    '''(experimental) Log configuration for a pipe.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html#eb-pipes-logs-level
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        # log_group: logs.LogGroup
        
        
        cwl_log_destination = pipes.CloudwatchLogsLogDestination(log_group)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=SqsTarget(target_queue),
            log_level=pipes.LogLevel.TRACE,
            log_include_execution_data=[pipes.IncludeExecutionData.ALL],
            log_destinations=[cwl_log_destination]
        )
    '''

    OFF = "OFF"
    '''(experimental) No logging.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) Log only errors.

    :stability: experimental
    '''
    INFO = "INFO"
    '''(experimental) Log errors, warnings, and info.

    :stability: experimental
    '''
    TRACE = "TRACE"
    '''(experimental) Log everything.

    :stability: experimental
    '''


@jsii.implements(IPipe)
class Pipe(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.Pipe",
):
    '''(experimental) Amazon EventBridge Pipes connects sources to targets.

    Pipes are intended for point-to-point integrations between supported sources and targets,
    with support for advanced transformations and enrichment.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html
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

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source: ISource,
        target: ITarget,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[DesiredState] = None,
        enrichment: typing.Optional[IEnrichment] = None,
        filter: typing.Optional[IFilter] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        log_destinations: typing.Optional[typing.Sequence[ILogDestination]] = None,
        log_include_execution_data: typing.Optional[typing.Sequence[IncludeExecutionData]] = None,
        log_level: typing.Optional[LogLevel] = None,
        pipe_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source: (experimental) The source of the pipe.
        :param target: (experimental) The target of the pipe.
        :param description: (experimental) A description of the pipe displayed in the AWS console. Default: - no description
        :param desired_state: (experimental) The desired state of the pipe. If the state is set to STOPPED, the pipe will not process events. Default: - DesiredState.RUNNING
        :param enrichment: (experimental) Enrichment step to enhance the data from the source before sending it to the target. Default: - no enrichment
        :param filter: (experimental) The filter pattern for the pipe source. Default: - no filter
        :param kms_key: (experimental) The AWS KMS customer managed key to encrypt pipe data. Default: undefined - AWS managed key is used
        :param log_destinations: (experimental) Destinations for the logs. Default: - no logs
        :param log_include_execution_data: (experimental) Whether the execution data (specifically, the ``payload`` , ``awsRequest`` , and ``awsResponse`` fields) is included in the log messages for this pipe. This applies to all log destinations for the pipe. For more information, see `Including execution data in logs <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html#eb-pipes-logs-execution-data>`_ and the `message schema <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs-schema.html>`_ in the *Amazon EventBridge User Guide* . Default: - none
        :param log_level: (experimental) The level of logging detail to include. This applies to all log destinations for the pipe. Default: - LogLevel.ERROR
        :param pipe_name: (experimental) Name of the pipe in the AWS console. Default: - automatically generated name
        :param role: (experimental) The role used by the pipe which has permissions to read from the source and write to the target. If an enriched target is used, the role also have permissions to call the enriched target. If no role is provided, a role will be created. Default: - a new role will be created.
        :param tags: (experimental) The list of key-value pairs to associate with the pipe. Default: - no tags

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a16b1ec145d1619299405f7b6191f4db9d8a48fea3ba0271aefd4dbf109992)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipeProps(
            source=source,
            target=target,
            description=description,
            desired_state=desired_state,
            enrichment=enrichment,
            filter=filter,
            kms_key=kms_key,
            log_destinations=log_destinations,
            log_include_execution_data=log_include_execution_data,
            log_level=log_level,
            pipe_name=pipe_name,
            role=role,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPipeName")
    @builtins.classmethod
    def from_pipe_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        pipe_name: builtins.str,
    ) -> IPipe:
        '''(experimental) Creates a pipe from the name of a pipe.

        :param scope: -
        :param id: -
        :param pipe_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa7e39cebf87a8ee866eef9f91d91e60ff66c487c1b13c721c07eb05a41ff40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pipe_name", value=pipe_name, expected_type=type_hints["pipe_name"])
        return typing.cast(IPipe, jsii.sinvoke(cls, "fromPipeName", [scope, id, pipe_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="pipeArn")
    def pipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the pipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "pipeArn"))

    @builtins.property
    @jsii.member(jsii_name="pipeName")
    def pipe_name(self) -> builtins.str:
        '''(experimental) The name of the pipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "pipeName"))

    @builtins.property
    @jsii.member(jsii_name="pipeRole")
    def pipe_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by the pipe.

        For imported pipes it assumes that the default role is used.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "pipeRole"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.PipeProps",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "description": "description",
        "desired_state": "desiredState",
        "enrichment": "enrichment",
        "filter": "filter",
        "kms_key": "kmsKey",
        "log_destinations": "logDestinations",
        "log_include_execution_data": "logIncludeExecutionData",
        "log_level": "logLevel",
        "pipe_name": "pipeName",
        "role": "role",
        "tags": "tags",
    },
)
class PipeProps:
    def __init__(
        self,
        *,
        source: ISource,
        target: ITarget,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[DesiredState] = None,
        enrichment: typing.Optional[IEnrichment] = None,
        filter: typing.Optional[IFilter] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        log_destinations: typing.Optional[typing.Sequence[ILogDestination]] = None,
        log_include_execution_data: typing.Optional[typing.Sequence[IncludeExecutionData]] = None,
        log_level: typing.Optional[LogLevel] = None,
        pipe_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for a pipe.

        :param source: (experimental) The source of the pipe.
        :param target: (experimental) The target of the pipe.
        :param description: (experimental) A description of the pipe displayed in the AWS console. Default: - no description
        :param desired_state: (experimental) The desired state of the pipe. If the state is set to STOPPED, the pipe will not process events. Default: - DesiredState.RUNNING
        :param enrichment: (experimental) Enrichment step to enhance the data from the source before sending it to the target. Default: - no enrichment
        :param filter: (experimental) The filter pattern for the pipe source. Default: - no filter
        :param kms_key: (experimental) The AWS KMS customer managed key to encrypt pipe data. Default: undefined - AWS managed key is used
        :param log_destinations: (experimental) Destinations for the logs. Default: - no logs
        :param log_include_execution_data: (experimental) Whether the execution data (specifically, the ``payload`` , ``awsRequest`` , and ``awsResponse`` fields) is included in the log messages for this pipe. This applies to all log destinations for the pipe. For more information, see `Including execution data in logs <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html#eb-pipes-logs-execution-data>`_ and the `message schema <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs-schema.html>`_ in the *Amazon EventBridge User Guide* . Default: - none
        :param log_level: (experimental) The level of logging detail to include. This applies to all log destinations for the pipe. Default: - LogLevel.ERROR
        :param pipe_name: (experimental) Name of the pipe in the AWS console. Default: - automatically generated name
        :param role: (experimental) The role used by the pipe which has permissions to read from the source and write to the target. If an enriched target is used, the role also have permissions to call the enriched target. If no role is provided, a role will be created. Default: - a new role will be created.
        :param tags: (experimental) The list of key-value pairs to associate with the pipe. Default: - no tags

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
            type_hints = typing.get_type_hints(_typecheckingstub__313bc6b11db2c5b2bd2ed71d515f3607669431a7c710ba93828cd389b2006357)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument enrichment", value=enrichment, expected_type=type_hints["enrichment"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument log_destinations", value=log_destinations, expected_type=type_hints["log_destinations"])
            check_type(argname="argument log_include_execution_data", value=log_include_execution_data, expected_type=type_hints["log_include_execution_data"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument pipe_name", value=pipe_name, expected_type=type_hints["pipe_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }
        if description is not None:
            self._values["description"] = description
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if enrichment is not None:
            self._values["enrichment"] = enrichment
        if filter is not None:
            self._values["filter"] = filter
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if log_destinations is not None:
            self._values["log_destinations"] = log_destinations
        if log_include_execution_data is not None:
            self._values["log_include_execution_data"] = log_include_execution_data
        if log_level is not None:
            self._values["log_level"] = log_level
        if pipe_name is not None:
            self._values["pipe_name"] = pipe_name
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def source(self) -> ISource:
        '''(experimental) The source of the pipe.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-source.html
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(ISource, result)

    @builtins.property
    def target(self) -> ITarget:
        '''(experimental) The target of the pipe.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html
        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(ITarget, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the pipe displayed in the AWS console.

        :default: - no description

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-description
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[DesiredState]:
        '''(experimental) The desired state of the pipe.

        If the state is set to STOPPED, the pipe will not process events.

        :default: - DesiredState.RUNNING

        :see: https://docs.aws.amazon.com/eventbridge/latest/pipes-reference/API_Pipe.html#eventbridge-Type-Pipe-DesiredState
        :stability: experimental
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[DesiredState], result)

    @builtins.property
    def enrichment(self) -> typing.Optional[IEnrichment]:
        '''(experimental) Enrichment step to enhance the data from the source before sending it to the target.

        :default: - no enrichment

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/pipes-enrichment.html
        :stability: experimental
        '''
        result = self._values.get("enrichment")
        return typing.cast(typing.Optional[IEnrichment], result)

    @builtins.property
    def filter(self) -> typing.Optional[IFilter]:
        '''(experimental) The filter pattern for the pipe source.

        :default: - no filter

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-filtering.html
        :stability: experimental
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[IFilter], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The AWS KMS customer managed key to encrypt pipe data.

        :default: undefined - AWS managed key is used

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def log_destinations(self) -> typing.Optional[typing.List[ILogDestination]]:
        '''(experimental) Destinations for the logs.

        :default: - no logs

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html
        :stability: experimental
        '''
        result = self._values.get("log_destinations")
        return typing.cast(typing.Optional[typing.List[ILogDestination]], result)

    @builtins.property
    def log_include_execution_data(
        self,
    ) -> typing.Optional[typing.List[IncludeExecutionData]]:
        '''(experimental) Whether the execution data (specifically, the ``payload`` , ``awsRequest`` , and ``awsResponse`` fields) is included in the log messages for this pipe.

        This applies to all log destinations for the pipe.

        For more information, see `Including execution data in logs <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html#eb-pipes-logs-execution-data>`_ and the `message schema <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs-schema.html>`_ in the *Amazon EventBridge User Guide* .

        :default: - none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-includeexecutiondata
        :stability: experimental
        '''
        result = self._values.get("log_include_execution_data")
        return typing.cast(typing.Optional[typing.List[IncludeExecutionData]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[LogLevel]:
        '''(experimental) The level of logging detail to include.

        This applies to all log destinations for the pipe.

        :default: - LogLevel.ERROR

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html
        :stability: experimental
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[LogLevel], result)

    @builtins.property
    def pipe_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the pipe in the AWS console.

        :default: - automatically generated name

        :stability: experimental
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-name
        '''
        result = self._values.get("pipe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role used by the pipe which has permissions to read from the source and write to the target.

        If an enriched target is used, the role also have permissions to call the enriched target.
        If no role is provided, a role will be created.

        :default: - a new role will be created.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-permissions.html
        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The list of key-value pairs to associate with the pipe.

        :default: - no tags

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-tags
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-alpha.PipeVariable")
class PipeVariable(enum.Enum):
    '''(experimental) Reserved pipe variables.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-input-transformation.html#input-transform-reserved
    :stability: experimental
    '''

    ARN = "ARN"
    '''(experimental) The Amazon Resource Name (ARN) of the pipe.

    :stability: experimental
    '''
    NAME = "NAME"
    '''(experimental) The name of the pipe.

    :stability: experimental
    '''
    SOURCE_ARN = "SOURCE_ARN"
    '''(experimental) The ARN of the event source of the pipe.

    :stability: experimental
    '''
    ENRICHMENT_ARN = "ENRICHMENT_ARN"
    '''(experimental) The ARN of the enrichment of the pipe.

    :stability: experimental
    '''
    TARGET_ARN = "TARGET_ARN"
    '''(experimental) The ARN of the target of the pipe.

    :stability: experimental
    '''
    EVENT_INGESTION_TIME = "EVENT_INGESTION_TIME"
    '''(experimental) The time at which the event was received by the input transformer.

    This is an ISO 8601 timestamp. This time is different for the enrichment input transformer and the target input transformer, depending on when the enrichment completed processing the event.

    :stability: experimental
    '''
    EVENT = "EVENT"
    '''(experimental) The event as received by the input transformer.

    :stability: experimental
    '''
    EVENT_JSON = "EVENT_JSON"
    '''(experimental) The same as aws.pipes.event, but the variable only has a value if the original payload, either from the source or returned by the enrichment, is JSON. If the pipe has an encoded field, such as the Amazon SQS body field or the Kinesis data, those fields are decoded and turned into valid JSON. Because it isn't escaped, the variable can only be used as a value for a JSON field. For more information, see Implicit body data parsing.

    :stability: experimental
    '''


@jsii.implements(ILogDestination)
class S3LogDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.S3LogDestination",
):
    '''(experimental) S3 bucket for delivery of pipe logs.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pipes_alpha as pipes_alpha
        from aws_cdk import aws_s3 as s3
        
        # bucket: s3.Bucket
        
        s3_log_destination = pipes_alpha.S3LogDestination(
            bucket=bucket,
        
            # the properties below are optional
            bucket_owner="bucketOwner",
            output_format=pipes_alpha.S3OutputFormat.PLAIN,
            prefix="prefix"
        )
    '''

    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        bucket_owner: typing.Optional[builtins.str] = None,
        output_format: typing.Optional["S3OutputFormat"] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: (experimental) The S3 bucket to deliver the log records for the pipe. The bucket can be in the same or a different AWS Account. If the bucket is in a different account, specify ``bucketOwner``. You must also allow access to the Pipes role in the bucket policy of the cross-account bucket.
        :param bucket_owner: (experimental) The AWS Account that owns the Amazon S3 bucket to which EventBridge delivers the log records for the pipe. Default: - account ID derived from ``bucket``
        :param output_format: (experimental) The format for the log records. Default: ``S3OutputFormat.JSON``
        :param prefix: (experimental) The prefix text with which to begin Amazon S3 log object names. Default: - no prefix

        :stability: experimental
        '''
        parameters = S3LogDestinationProps(
            bucket=bucket,
            bucket_owner=bucket_owner,
            output_format=output_format,
            prefix=prefix,
        )

        jsii.create(self.__class__, self, [parameters])

    @jsii.member(jsii_name="bind")
    def bind(self, _pipe: IPipe) -> LogDestinationConfig:
        '''(experimental) Bind the log destination to the pipe.

        :param _pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cd4e9c3fd8ddb334a7abaf91523ebe83e613b68575169b6cf626f85654953a)
            check_type(argname="argument _pipe", value=_pipe, expected_type=type_hints["_pipe"])
        return typing.cast(LogDestinationConfig, jsii.invoke(self, "bind", [_pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, pipe_role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the log destination.

        :param pipe_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bf0ef0579df52d09687546d2e08d9fece7a560fcbdfdbd733ed87c66718026)
            check_type(argname="argument pipe_role", value=pipe_role, expected_type=type_hints["pipe_role"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [pipe_role]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.S3LogDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "bucket_owner": "bucketOwner",
        "output_format": "outputFormat",
        "prefix": "prefix",
    },
)
class S3LogDestinationProps:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        bucket_owner: typing.Optional[builtins.str] = None,
        output_format: typing.Optional["S3OutputFormat"] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for ``S3LogDestination``.

        :param bucket: (experimental) The S3 bucket to deliver the log records for the pipe. The bucket can be in the same or a different AWS Account. If the bucket is in a different account, specify ``bucketOwner``. You must also allow access to the Pipes role in the bucket policy of the cross-account bucket.
        :param bucket_owner: (experimental) The AWS Account that owns the Amazon S3 bucket to which EventBridge delivers the log records for the pipe. Default: - account ID derived from ``bucket``
        :param output_format: (experimental) The format for the log records. Default: ``S3OutputFormat.JSON``
        :param prefix: (experimental) The prefix text with which to begin Amazon S3 log object names. Default: - no prefix

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            from aws_cdk import aws_s3 as s3
            
            # bucket: s3.Bucket
            
            s3_log_destination_props = pipes_alpha.S3LogDestinationProps(
                bucket=bucket,
            
                # the properties below are optional
                bucket_owner="bucketOwner",
                output_format=pipes_alpha.S3OutputFormat.PLAIN,
                prefix="prefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68166b3af630b15e997251f1748de9b008b044f716f5007322fb208988832fab)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if bucket_owner is not None:
            self._values["bucket_owner"] = bucket_owner
        if output_format is not None:
            self._values["output_format"] = output_format
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The S3 bucket to deliver the log records for the pipe.

        The bucket can be in the same or a different AWS Account. If the bucket is in
        a different account, specify ``bucketOwner``. You must also allow access to the
        Pipes role in the bucket policy of the cross-account bucket.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-bucketname
        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def bucket_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS Account that owns the Amazon S3 bucket to which EventBridge delivers the log records for the pipe.

        :default: - account ID derived from ``bucket``

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-bucketowner
        :stability: experimental
        '''
        result = self._values.get("bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_format(self) -> typing.Optional["S3OutputFormat"]:
        '''(experimental) The format for the log records.

        :default: ``S3OutputFormat.JSON``

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-outputformat
        :stability: experimental
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional["S3OutputFormat"], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix text with which to begin Amazon S3 log object names.

        :default: - no prefix

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-prefix
        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3LogDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-alpha.S3OutputFormat")
class S3OutputFormat(enum.Enum):
    '''(experimental) Log format for ``S3LogDestination`` logging configuration.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-outputformat
    :stability: experimental
    '''

    PLAIN = "PLAIN"
    '''(experimental) Plain text.

    :stability: experimental
    '''
    JSON = "JSON"
    '''(experimental) JSON.

    :stability: experimental
    '''
    W3C = "W3C"
    '''(experimental) W3C extended log file format.

    :see: https://www.w3.org/TR/WD-logfile
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={"source_parameters": "sourceParameters"},
)
class SourceConfig:
    def __init__(
        self,
        *,
        source_parameters: typing.Optional[typing.Union["SourceParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Source properties.

        :param source_parameters: (experimental) The parameters required to set up a source for your pipe. Default: - none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            
            source_config = pipes_alpha.SourceConfig(
                source_parameters=pipes_alpha.SourceParameters(
                    active_mq_broker_parameters=PipeSourceActiveMQBrokerParametersProperty(
                        credentials=MQBrokerAccessCredentialsProperty(
                            basic_auth="basicAuth"
                        ),
                        queue_name="queueName",
            
                        # the properties below are optional
                        batch_size=123,
                        maximum_batching_window_in_seconds=123
                    ),
                    dynamo_db_stream_parameters=PipeSourceDynamoDBStreamParametersProperty(
                        starting_position="startingPosition",
            
                        # the properties below are optional
                        batch_size=123,
                        dead_letter_config=DeadLetterConfigProperty(
                            arn="arn"
                        ),
                        maximum_batching_window_in_seconds=123,
                        maximum_record_age_in_seconds=123,
                        maximum_retry_attempts=123,
                        on_partial_batch_item_failure="onPartialBatchItemFailure",
                        parallelization_factor=123
                    ),
                    kinesis_stream_parameters=PipeSourceKinesisStreamParametersProperty(
                        starting_position="startingPosition",
            
                        # the properties below are optional
                        batch_size=123,
                        dead_letter_config=DeadLetterConfigProperty(
                            arn="arn"
                        ),
                        maximum_batching_window_in_seconds=123,
                        maximum_record_age_in_seconds=123,
                        maximum_retry_attempts=123,
                        on_partial_batch_item_failure="onPartialBatchItemFailure",
                        parallelization_factor=123,
                        starting_position_timestamp="startingPositionTimestamp"
                    ),
                    managed_streaming_kafka_parameters=PipeSourceManagedStreamingKafkaParametersProperty(
                        topic_name="topicName",
            
                        # the properties below are optional
                        batch_size=123,
                        consumer_group_id="consumerGroupId",
                        credentials=MSKAccessCredentialsProperty(
                            client_certificate_tls_auth="clientCertificateTlsAuth",
                            sasl_scram512_auth="saslScram512Auth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        starting_position="startingPosition"
                    ),
                    rabbit_mq_broker_parameters=PipeSourceRabbitMQBrokerParametersProperty(
                        credentials=MQBrokerAccessCredentialsProperty(
                            basic_auth="basicAuth"
                        ),
                        queue_name="queueName",
            
                        # the properties below are optional
                        batch_size=123,
                        maximum_batching_window_in_seconds=123,
                        virtual_host="virtualHost"
                    ),
                    self_managed_kafka_parameters=PipeSourceSelfManagedKafkaParametersProperty(
                        topic_name="topicName",
            
                        # the properties below are optional
                        additional_bootstrap_servers=["additionalBootstrapServers"],
                        batch_size=123,
                        consumer_group_id="consumerGroupId",
                        credentials=SelfManagedKafkaAccessConfigurationCredentialsProperty(
                            basic_auth="basicAuth",
                            client_certificate_tls_auth="clientCertificateTlsAuth",
                            sasl_scram256_auth="saslScram256Auth",
                            sasl_scram512_auth="saslScram512Auth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        server_root_ca_certificate="serverRootCaCertificate",
                        starting_position="startingPosition",
                        vpc=SelfManagedKafkaAccessConfigurationVpcProperty(
                            security_group=["securityGroup"],
                            subnets=["subnets"]
                        )
                    ),
                    sqs_queue_parameters=PipeSourceSqsQueueParametersProperty(
                        batch_size=123,
                        maximum_batching_window_in_seconds=123
                    )
                )
            )
        '''
        if isinstance(source_parameters, dict):
            source_parameters = SourceParameters(**source_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f844d2947870fbd6fb6f50ffeb0235eb88a7ec9a57df944902c83483f8b6969e)
            check_type(argname="argument source_parameters", value=source_parameters, expected_type=type_hints["source_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_parameters is not None:
            self._values["source_parameters"] = source_parameters

    @builtins.property
    def source_parameters(self) -> typing.Optional["SourceParameters"]:
        '''(experimental) The parameters required to set up a source for your pipe.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("source_parameters")
        return typing.cast(typing.Optional["SourceParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.SourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "active_mq_broker_parameters": "activeMqBrokerParameters",
        "dynamo_db_stream_parameters": "dynamoDbStreamParameters",
        "kinesis_stream_parameters": "kinesisStreamParameters",
        "managed_streaming_kafka_parameters": "managedStreamingKafkaParameters",
        "rabbit_mq_broker_parameters": "rabbitMqBrokerParameters",
        "self_managed_kafka_parameters": "selfManagedKafkaParameters",
        "sqs_queue_parameters": "sqsQueueParameters",
    },
)
class SourceParameters:
    def __init__(
        self,
        *,
        active_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceActiveMQBrokerParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        dynamo_db_stream_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceDynamoDBStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceKinesisStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        managed_streaming_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceManagedStreamingKafkaParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        rabbit_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceRabbitMQBrokerParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSelfManagedKafkaParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSqsQueueParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Source properties.

        :param active_mq_broker_parameters: (experimental) ActiveMQBroker configuration parameters. Default: - none
        :param dynamo_db_stream_parameters: (experimental) DynamoDB stream configuration parameters. Default: - none
        :param kinesis_stream_parameters: (experimental) Kinesis stream configuration parameters. Default: - none
        :param managed_streaming_kafka_parameters: (experimental) Managed streaming Kafka configuration parameters. Default: - none
        :param rabbit_mq_broker_parameters: (experimental) RabbitMQ broker configuration parameters. Default: - none
        :param self_managed_kafka_parameters: (experimental) Self-managed Kafka configuration parameters. Default: - none
        :param sqs_queue_parameters: (experimental) SQS queue configuration parameters. Default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-source.html
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
        if isinstance(active_mq_broker_parameters, dict):
            active_mq_broker_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceActiveMQBrokerParametersProperty(**active_mq_broker_parameters)
        if isinstance(dynamo_db_stream_parameters, dict):
            dynamo_db_stream_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceDynamoDBStreamParametersProperty(**dynamo_db_stream_parameters)
        if isinstance(kinesis_stream_parameters, dict):
            kinesis_stream_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceKinesisStreamParametersProperty(**kinesis_stream_parameters)
        if isinstance(managed_streaming_kafka_parameters, dict):
            managed_streaming_kafka_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceManagedStreamingKafkaParametersProperty(**managed_streaming_kafka_parameters)
        if isinstance(rabbit_mq_broker_parameters, dict):
            rabbit_mq_broker_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceRabbitMQBrokerParametersProperty(**rabbit_mq_broker_parameters)
        if isinstance(self_managed_kafka_parameters, dict):
            self_managed_kafka_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSelfManagedKafkaParametersProperty(**self_managed_kafka_parameters)
        if isinstance(sqs_queue_parameters, dict):
            sqs_queue_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSqsQueueParametersProperty(**sqs_queue_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199f5cdcd17c493da5309249fbe2bf553db5fe7501e100c178ce58b130724435)
            check_type(argname="argument active_mq_broker_parameters", value=active_mq_broker_parameters, expected_type=type_hints["active_mq_broker_parameters"])
            check_type(argname="argument dynamo_db_stream_parameters", value=dynamo_db_stream_parameters, expected_type=type_hints["dynamo_db_stream_parameters"])
            check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
            check_type(argname="argument managed_streaming_kafka_parameters", value=managed_streaming_kafka_parameters, expected_type=type_hints["managed_streaming_kafka_parameters"])
            check_type(argname="argument rabbit_mq_broker_parameters", value=rabbit_mq_broker_parameters, expected_type=type_hints["rabbit_mq_broker_parameters"])
            check_type(argname="argument self_managed_kafka_parameters", value=self_managed_kafka_parameters, expected_type=type_hints["self_managed_kafka_parameters"])
            check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_mq_broker_parameters is not None:
            self._values["active_mq_broker_parameters"] = active_mq_broker_parameters
        if dynamo_db_stream_parameters is not None:
            self._values["dynamo_db_stream_parameters"] = dynamo_db_stream_parameters
        if kinesis_stream_parameters is not None:
            self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
        if managed_streaming_kafka_parameters is not None:
            self._values["managed_streaming_kafka_parameters"] = managed_streaming_kafka_parameters
        if rabbit_mq_broker_parameters is not None:
            self._values["rabbit_mq_broker_parameters"] = rabbit_mq_broker_parameters
        if self_managed_kafka_parameters is not None:
            self._values["self_managed_kafka_parameters"] = self_managed_kafka_parameters
        if sqs_queue_parameters is not None:
            self._values["sqs_queue_parameters"] = sqs_queue_parameters

    @builtins.property
    def active_mq_broker_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceActiveMQBrokerParametersProperty]:
        '''(experimental) ActiveMQBroker configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-mq.html
        :stability: experimental
        '''
        result = self._values.get("active_mq_broker_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceActiveMQBrokerParametersProperty], result)

    @builtins.property
    def dynamo_db_stream_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceDynamoDBStreamParametersProperty]:
        '''(experimental) DynamoDB stream configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html
        :stability: experimental
        '''
        result = self._values.get("dynamo_db_stream_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceDynamoDBStreamParametersProperty], result)

    @builtins.property
    def kinesis_stream_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceKinesisStreamParametersProperty]:
        '''(experimental) Kinesis stream configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kinesis.html
        :stability: experimental
        '''
        result = self._values.get("kinesis_stream_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceKinesisStreamParametersProperty], result)

    @builtins.property
    def managed_streaming_kafka_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceManagedStreamingKafkaParametersProperty]:
        '''(experimental) Managed streaming Kafka configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-msk.html
        :stability: experimental
        '''
        result = self._values.get("managed_streaming_kafka_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceManagedStreamingKafkaParametersProperty], result)

    @builtins.property
    def rabbit_mq_broker_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceRabbitMQBrokerParametersProperty]:
        '''(experimental) RabbitMQ broker configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-mq.html
        :stability: experimental
        '''
        result = self._values.get("rabbit_mq_broker_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceRabbitMQBrokerParametersProperty], result)

    @builtins.property
    def self_managed_kafka_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSelfManagedKafkaParametersProperty]:
        '''(experimental) Self-managed Kafka configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kafka.html
        :stability: experimental
        '''
        result = self._values.get("self_managed_kafka_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSelfManagedKafkaParametersProperty], result)

    @builtins.property
    def sqs_queue_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSqsQueueParametersProperty]:
        '''(experimental) SQS queue configuration parameters.

        :default: - none

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-sqs.html
        :stability: experimental
        '''
        result = self._values.get("sqs_queue_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSqsQueueParametersProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISource)
class SourceWithDeadLetterTarget(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-pipes-alpha.SourceWithDeadLetterTarget",
):
    '''(experimental) Sources that support a dead-letter target.

    :stability: experimental
    '''

    def __init__(
        self,
        source_arn: builtins.str,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    ) -> None:
        '''
        :param source_arn: The ARN of the source resource.
        :param dead_letter_target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ecd2a601b556b5b4bd20a7ca1fe7f0d8dd3b3163d1f720a1d2a85292c37697)
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument dead_letter_target", value=dead_letter_target, expected_type=type_hints["dead_letter_target"])
        jsii.create(self.__class__, self, [source_arn, dead_letter_target])

    @jsii.member(jsii_name="isSourceWithDeadLetterTarget")
    @builtins.classmethod
    def is_source_with_dead_letter_target(cls, source: ISource) -> builtins.bool:
        '''(experimental) Determines if the source is an instance of SourceWithDeadLetterTarget.

        :param source: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ce37fa312e488d05c4159a0b21b6cc6382fe0ca98b8292cd7b8b8c1fa49744)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isSourceWithDeadLetterTarget", [source]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, pipe: IPipe) -> SourceConfig:
        '''(experimental) Bind the source to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="getDeadLetterTargetArn")
    def _get_dead_letter_target_arn(
        self,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Retrieves the ARN from the dead-letter SQS queue or SNS topic.

        :param dead_letter_target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f884fdf28794088e22141c13254afebc133495d9c30ecf2f14f3dad5f3d0fdb9)
            check_type(argname="argument dead_letter_target", value=dead_letter_target, expected_type=type_hints["dead_letter_target"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getDeadLetterTargetArn", [dead_letter_target]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    ) -> None:
        '''(experimental) Grants the pipe role permission to publish to the dead-letter target.

        :param grantee: -
        :param dead_letter_target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10839b775175ef29c4896a58b0c102a4e136ecffe8d192a7a3affb72ced25849)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument dead_letter_target", value=dead_letter_target, expected_type=type_hints["dead_letter_target"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee, dead_letter_target]))

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''(experimental) The ARN of the source resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterTarget")
    def dead_letter_target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]]:
        '''(experimental) The dead-letter SQS queue or SNS topic.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]], jsii.get(self, "deadLetterTarget"))


class _SourceWithDeadLetterTargetProxy(SourceWithDeadLetterTarget):
    @jsii.member(jsii_name="bind")
    def bind(self, pipe: IPipe) -> SourceConfig:
        '''(experimental) Bind the source to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db7b2a16c569bd951d9560c3d807b9ef7233b3af52810b44775141e7f17bbf4)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(SourceConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16ef93508f1d041b3a420b7293f59cdae8749cfd2d8321bdaded86f6f4b6e99)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SourceWithDeadLetterTarget).__jsii_proxy_class__ = lambda : _SourceWithDeadLetterTargetProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-alpha.TargetConfig",
    jsii_struct_bases=[],
    name_mapping={"target_parameters": "targetParameters"},
)
class TargetConfig:
    def __init__(
        self,
        *,
        target_parameters: typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeTargetParametersProperty, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Target config properties.

        :param target_parameters: (experimental) The parameters required to set up a target for your pipe.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_alpha as pipes_alpha
            
            target_config = pipes_alpha.TargetConfig(
                target_parameters=PipeTargetParametersProperty(
                    batch_job_parameters=PipeTargetBatchJobParametersProperty(
                        job_definition="jobDefinition",
                        job_name="jobName",
            
                        # the properties below are optional
                        array_properties=BatchArrayPropertiesProperty(
                            size=123
                        ),
                        container_overrides=BatchContainerOverridesProperty(
                            command=["command"],
                            environment=[BatchEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            instance_type="instanceType",
                            resource_requirements=[BatchResourceRequirementProperty(
                                type="type",
                                value="value"
                            )]
                        ),
                        depends_on=[BatchJobDependencyProperty(
                            job_id="jobId",
                            type="type"
                        )],
                        parameters={
                            "parameters_key": "parameters"
                        },
                        retry_strategy=BatchRetryStrategyProperty(
                            attempts=123
                        )
                    ),
                    cloud_watch_logs_parameters=PipeTargetCloudWatchLogsParametersProperty(
                        log_stream_name="logStreamName",
                        timestamp="timestamp"
                    ),
                    ecs_task_parameters=PipeTargetEcsTaskParametersProperty(
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
                        overrides=EcsTaskOverrideProperty(
                            container_overrides=[EcsContainerOverrideProperty(
                                command=["command"],
                                cpu=123,
                                environment=[EcsEnvironmentVariableProperty(
                                    name="name",
                                    value="value"
                                )],
                                environment_files=[EcsEnvironmentFileProperty(
                                    type="type",
                                    value="value"
                                )],
                                memory=123,
                                memory_reservation=123,
                                name="name",
                                resource_requirements=[EcsResourceRequirementProperty(
                                    type="type",
                                    value="value"
                                )]
                            )],
                            cpu="cpu",
                            ephemeral_storage=EcsEphemeralStorageProperty(
                                size_in_gi_b=123
                            ),
                            execution_role_arn="executionRoleArn",
                            inference_accelerator_overrides=[EcsInferenceAcceleratorOverrideProperty(
                                device_name="deviceName",
                                device_type="deviceType"
                            )],
                            memory="memory",
                            task_role_arn="taskRoleArn"
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
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        task_count=123
                    ),
                    event_bridge_event_bus_parameters=PipeTargetEventBridgeEventBusParametersProperty(
                        detail_type="detailType",
                        endpoint_id="endpointId",
                        resources=["resources"],
                        source="source",
                        time="time"
                    ),
                    http_parameters=PipeTargetHttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input_template="inputTemplate",
                    kinesis_stream_parameters=PipeTargetKinesisStreamParametersProperty(
                        partition_key="partitionKey"
                    ),
                    lambda_function_parameters=PipeTargetLambdaFunctionParametersProperty(
                        invocation_type="invocationType"
                    ),
                    redshift_data_parameters=PipeTargetRedshiftDataParametersProperty(
                        database="database",
                        sqls=["sqls"],
            
                        # the properties below are optional
                        db_user="dbUser",
                        secret_manager_arn="secretManagerArn",
                        statement_name="statementName",
                        with_event=False
                    ),
                    sage_maker_pipeline_parameters=PipeTargetSageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_queue_parameters=PipeTargetSqsQueueParametersProperty(
                        message_deduplication_id="messageDeduplicationId",
                        message_group_id="messageGroupId"
                    ),
                    step_function_state_machine_parameters=PipeTargetStateMachineParametersProperty(
                        invocation_type="invocationType"
                    ),
                    timestream_parameters=PipeTargetTimestreamParametersProperty(
                        dimension_mappings=[DimensionMappingProperty(
                            dimension_name="dimensionName",
                            dimension_value="dimensionValue",
                            dimension_value_type="dimensionValueType"
                        )],
                        time_value="timeValue",
                        version_value="versionValue",
            
                        # the properties below are optional
                        epoch_time_unit="epochTimeUnit",
                        multi_measure_mappings=[MultiMeasureMappingProperty(
                            multi_measure_attribute_mappings=[MultiMeasureAttributeMappingProperty(
                                measure_value="measureValue",
                                measure_value_type="measureValueType",
                                multi_measure_attribute_name="multiMeasureAttributeName"
                            )],
                            multi_measure_name="multiMeasureName"
                        )],
                        single_measure_mappings=[SingleMeasureMappingProperty(
                            measure_name="measureName",
                            measure_value="measureValue",
                            measure_value_type="measureValueType"
                        )],
                        time_field_type="timeFieldType",
                        timestamp_format="timestampFormat"
                    )
                )
            )
        '''
        if isinstance(target_parameters, dict):
            target_parameters = _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeTargetParametersProperty(**target_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16786968bb2f48da037c06a4ec6792643f6244fa0aec73521fb6c15685387f83)
            check_type(argname="argument target_parameters", value=target_parameters, expected_type=type_hints["target_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_parameters": target_parameters,
        }

    @builtins.property
    def target_parameters(
        self,
    ) -> _aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeTargetParametersProperty:
        '''(experimental) The parameters required to set up a target for your pipe.

        :stability: experimental
        '''
        result = self._values.get("target_parameters")
        assert result is not None, "Required property 'target_parameters' is missing"
        return typing.cast(_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeTargetParametersProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TargetParameter(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.TargetParameter",
):
    '''(experimental) Define dynamic target parameters.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pipes_alpha as pipes_alpha
        
        target_parameter = pipes_alpha.TargetParameter()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromJsonPath")
    @builtins.classmethod
    def from_json_path(cls, json_path: builtins.str) -> builtins.str:
        '''(experimental) Target parameter based on a jsonPath expression from the incoming event.

        :param json_path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6175e65e10c71e88fc9736f275d598e53162777097410454a3bb9356d9218ad)
            check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromJsonPath", [json_path]))


@jsii.implements(ILogDestination)
class CloudwatchLogsLogDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.CloudwatchLogsLogDestination",
):
    '''(experimental) CloudWatch Logs log group for delivery of pipe logs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        # log_group: logs.LogGroup
        
        
        cwl_log_destination = pipes.CloudwatchLogsLogDestination(log_group)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=SqsTarget(target_queue),
            log_level=pipes.LogLevel.TRACE,
            log_include_execution_data=[pipes.IncludeExecutionData.ALL],
            log_destinations=[cwl_log_destination]
        )
    '''

    def __init__(self, log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup) -> None:
        '''
        :param log_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7349adb8d269e5dfcc7e2977d1e8f8b7169762a1d65900645cd57cb9b72d2664)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        jsii.create(self.__class__, self, [log_group])

    @jsii.member(jsii_name="bind")
    def bind(self, _pipe: IPipe) -> LogDestinationConfig:
        '''(experimental) Bind the log destination to the pipe.

        :param _pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2476a0c2516678c5cb8a25042028c2f1369a921cdf123728612f66c57d39181b)
            check_type(argname="argument _pipe", value=_pipe, expected_type=type_hints["_pipe"])
        return typing.cast(LogDestinationConfig, jsii.invoke(self, "bind", [_pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, pipe_role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the log destination.

        :param pipe_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d5cdf451f256dd4861f4be2ad352486a7d4daea0c960d3ada8a70a0a9542e0)
            check_type(argname="argument pipe_role", value=pipe_role, expected_type=type_hints["pipe_role"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [pipe_role]))


@jsii.implements(IFilter)
class Filter(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-pipes-alpha.Filter"):
    '''(experimental) The collection of event patterns used to filter events.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        
        
        source_filter = pipes.Filter([
            pipes.FilterPattern.from_object({
                "body": {
                    # only forward events with customerType B2B or B2C
                    "customer_type": ["B2B", "B2C"]
                }
            })
        ])
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=SqsTarget(target_queue),
            filter=source_filter
        )
    '''

    def __init__(self, filter: typing.Sequence[IFilterPattern]) -> None:
        '''
        :param filter: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457f1df4cc78eb50117dee67a8b0d5c23731e52baf59ea09285951777d63fed4)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        jsii.create(self.__class__, self, [filter])

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.List[IFilterPattern]:
        '''(experimental) Filters for the source.

        :stability: experimental
        '''
        return typing.cast(typing.List[IFilterPattern], jsii.get(self, "filters"))

    @filters.setter
    def filters(self, value: typing.List[IFilterPattern]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121a40cea1baf9cf86e7a293c8a54161be711d421db1b0eb7f5531719d1bd324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value) # pyright: ignore[reportArgumentType]


@jsii.implements(ILogDestination)
class FirehoseLogDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-alpha.FirehoseLogDestination",
):
    '''(experimental) Firehose stream for delivery of pipe logs.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_pipes_alpha as pipes_alpha
        from aws_cdk import aws_kinesisfirehose as kinesisfirehose
        
        # delivery_stream: kinesisfirehose.DeliveryStream
        
        firehose_log_destination = pipes_alpha.FirehoseLogDestination(delivery_stream)
    '''

    def __init__(
        self,
        delivery_stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
    ) -> None:
        '''
        :param delivery_stream: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4e17f2ca915cd241cec254eff470fdb1a956f64fbdac6fb2f89b34f717718d)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        jsii.create(self.__class__, self, [delivery_stream])

    @jsii.member(jsii_name="bind")
    def bind(self, _pipe: IPipe) -> LogDestinationConfig:
        '''(experimental) Bind the log destination to the pipe.

        :param _pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680ad98836387c751dc6eec1f080c8b5facea0f989ced1a23d17dd6e2f323f58)
            check_type(argname="argument _pipe", value=_pipe, expected_type=type_hints["_pipe"])
        return typing.cast(LogDestinationConfig, jsii.invoke(self, "bind", [_pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, pipe_role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the log destination.

        :param pipe_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d247899f4ca74409b2a7b5dd44ad62df7b7b6a076af7cb21cc27a2f018fb54)
            check_type(argname="argument pipe_role", value=pipe_role, expected_type=type_hints["pipe_role"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [pipe_role]))


__all__ = [
    "CloudwatchLogsLogDestination",
    "DesiredState",
    "DynamicInput",
    "EnrichmentParametersConfig",
    "Filter",
    "FilterPattern",
    "FirehoseLogDestination",
    "IEnrichment",
    "IFilter",
    "IFilterPattern",
    "IInputTransformation",
    "ILogDestination",
    "IPipe",
    "ISource",
    "ITarget",
    "IncludeExecutionData",
    "InputTransformation",
    "InputTransformationConfig",
    "LogDestinationConfig",
    "LogDestinationParameters",
    "LogLevel",
    "Pipe",
    "PipeProps",
    "PipeVariable",
    "S3LogDestination",
    "S3LogDestinationProps",
    "S3OutputFormat",
    "SourceConfig",
    "SourceParameters",
    "SourceWithDeadLetterTarget",
    "TargetConfig",
    "TargetParameter",
]

publication.publish()

def _typecheckingstub__3c5bbb77d96c2570787e5e35a986888ea8bb0bc2ddd772916e47d846e4af16c2(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860e63dc447cbad7fc641786dc20a0b496495e9b8a1a5bfe862a8b2ed5672a0d(
    _context: _aws_cdk_ceddda9d.IResolveContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be50f45da4d8fc1e4aa1b783ed4d3d35da416296c1f3527ebe16e9c865a00a1f(
    *,
    enrichment_parameters: typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeEnrichmentParametersProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bd3fb3b0ffe9a4d7e3fe32ab50edde2c475b6ce11cad8df1ada38d5e3ad115(
    pattern_object: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc5492815137155b1832922d330923c5324c2144c6b7ce6f629cc5e40f4a455(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1ad4c7fe348a9788b14ee41d1c66c13826fc937049e66fdf554ed83bfe7baf(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d300fa623a25928741c7906df5849b8fe94e2c857016ddc27c9bfa606840c3(
    value: typing.List[IFilterPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c692a10525cf42d6819fccf1ba8a1c1a5e2c95948fc2df661221cdb6a2669568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c56b2ae871eaf486f0abeb0df58eb5ca1718e69de303cf680b518c5b755040(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fc07eda1cf81cdd6181b1c56681e9296a86e8c0e3831080bff1759881ddb5c(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e82ee136087b77e6440c7ba18e27a104e108c7b4e2fdc3b9347dc967f7e550(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc51442e0b59cd40f4211e4205ed3feaa6ab35fd337c948849a7fc75d273bea(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b7f3713c7dd058bbfa6fd41eff30b60ed5cd0026f7f24037edc7503d1d833c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e93dc435b6334c19ccf66163b6aad3d46712c8f63afc72a3d5267c12e8335b(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cc64b1eb25062d3fcee449052e46d0ae2ef8f2a0ee990643ee2c9cbfb79aa1(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182c04a131444303df0e217e3900a484fbc6ca8845dd17981187d035c3aa3054(
    json_path_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2bb77e9adef2b6e1b25daac546880929aa3cc34ea9887fe45d38161dc8a805(
    input_template: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fa91b1b3adb6b7383532aa0abf70cabcdfb70451cff3e408cb68ce7373f99d(
    input_template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9928c7373e9e39af7fd3151eb77ece0c9a46ed64f6c611d61ea7d11d51c02213(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630bec5abec8acb015b6dae32bfdea83eebf4822e821d1d788f9f55a4d3283c1(
    *,
    input_template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c221263227417f49ed8ca8afd4f2ca6238bec626c6b82c6ad0384b5e9cca219(
    *,
    parameters: typing.Union[LogDestinationParameters, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e011cd2ae75207e0b7e6eec35a33b026d9aa2fefab7715f3111f5d14739cc3(
    *,
    cloudwatch_logs_log_destination: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.CloudwatchLogsLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose_log_destination: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.FirehoseLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_log_destination: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.S3LogDestinationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a16b1ec145d1619299405f7b6191f4db9d8a48fea3ba0271aefd4dbf109992(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source: ISource,
    target: ITarget,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[DesiredState] = None,
    enrichment: typing.Optional[IEnrichment] = None,
    filter: typing.Optional[IFilter] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    log_destinations: typing.Optional[typing.Sequence[ILogDestination]] = None,
    log_include_execution_data: typing.Optional[typing.Sequence[IncludeExecutionData]] = None,
    log_level: typing.Optional[LogLevel] = None,
    pipe_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa7e39cebf87a8ee866eef9f91d91e60ff66c487c1b13c721c07eb05a41ff40(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    pipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313bc6b11db2c5b2bd2ed71d515f3607669431a7c710ba93828cd389b2006357(
    *,
    source: ISource,
    target: ITarget,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[DesiredState] = None,
    enrichment: typing.Optional[IEnrichment] = None,
    filter: typing.Optional[IFilter] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    log_destinations: typing.Optional[typing.Sequence[ILogDestination]] = None,
    log_include_execution_data: typing.Optional[typing.Sequence[IncludeExecutionData]] = None,
    log_level: typing.Optional[LogLevel] = None,
    pipe_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cd4e9c3fd8ddb334a7abaf91523ebe83e613b68575169b6cf626f85654953a(
    _pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bf0ef0579df52d09687546d2e08d9fece7a560fcbdfdbd733ed87c66718026(
    pipe_role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68166b3af630b15e997251f1748de9b008b044f716f5007322fb208988832fab(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    bucket_owner: typing.Optional[builtins.str] = None,
    output_format: typing.Optional[S3OutputFormat] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f844d2947870fbd6fb6f50ffeb0235eb88a7ec9a57df944902c83483f8b6969e(
    *,
    source_parameters: typing.Optional[typing.Union[SourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199f5cdcd17c493da5309249fbe2bf553db5fe7501e100c178ce58b130724435(
    *,
    active_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceActiveMQBrokerParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamo_db_stream_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceDynamoDBStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceKinesisStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_streaming_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceManagedStreamingKafkaParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    rabbit_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceRabbitMQBrokerParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSelfManagedKafkaParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeSourceSqsQueueParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ecd2a601b556b5b4bd20a7ca1fe7f0d8dd3b3163d1f720a1d2a85292c37697(
    source_arn: builtins.str,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ce37fa312e488d05c4159a0b21b6cc6382fe0ca98b8292cd7b8b8c1fa49744(
    source: ISource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f884fdf28794088e22141c13254afebc133495d9c30ecf2f14f3dad5f3d0fdb9(
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10839b775175ef29c4896a58b0c102a4e136ecffe8d192a7a3affb72ced25849(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db7b2a16c569bd951d9560c3d807b9ef7233b3af52810b44775141e7f17bbf4(
    pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16ef93508f1d041b3a420b7293f59cdae8749cfd2d8321bdaded86f6f4b6e99(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16786968bb2f48da037c06a4ec6792643f6244fa0aec73521fb6c15685387f83(
    *,
    target_parameters: typing.Union[_aws_cdk_aws_pipes_ceddda9d.CfnPipe.PipeTargetParametersProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6175e65e10c71e88fc9736f275d598e53162777097410454a3bb9356d9218ad(
    json_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7349adb8d269e5dfcc7e2977d1e8f8b7169762a1d65900645cd57cb9b72d2664(
    log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2476a0c2516678c5cb8a25042028c2f1369a921cdf123728612f66c57d39181b(
    _pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d5cdf451f256dd4861f4be2ad352486a7d4daea0c960d3ada8a70a0a9542e0(
    pipe_role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457f1df4cc78eb50117dee67a8b0d5c23731e52baf59ea09285951777d63fed4(
    filter: typing.Sequence[IFilterPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121a40cea1baf9cf86e7a293c8a54161be711d421db1b0eb7f5531719d1bd324(
    value: typing.List[IFilterPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4e17f2ca915cd241cec254eff470fdb1a956f64fbdac6fb2f89b34f717718d(
    delivery_stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680ad98836387c751dc6eec1f080c8b5facea0f989ced1a23d17dd6e2f323f58(
    _pipe: IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d247899f4ca74409b2a7b5dd44ad62df7b7b6a076af7cb21cc27a2f018fb54(
    pipe_role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass
