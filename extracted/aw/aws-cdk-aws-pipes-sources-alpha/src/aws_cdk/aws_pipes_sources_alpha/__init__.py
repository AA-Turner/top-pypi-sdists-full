r'''
# Amazon EventBridge Pipes Sources Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

EventBridge Pipes Sources let you create a source for a EventBridge Pipe.

For more details see the service documentation:

[Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-source.html)

## Pipe sources

Pipe sources are the starting point of a EventBridge Pipe. They are the source of the events that are sent to the pipe.

### Amazon SQS

A SQS message queue can be used as a source for a pipe. The queue will be polled for new messages and the messages will be sent to the pipe.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_source = sources.SqsSource(source_queue)

pipe = pipes.Pipe(self, "Pipe",
    source=pipe_source,
    target=SqsTarget(target_queue)
)
```

The polling configuration can be customized:

```python
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
```

### Amazon Kinesis

A Kinesis stream can be used as a source for a pipe. The stream will be polled for new messages and the messages will be sent to the pipe.

```python
# source_stream: kinesis.Stream
# target_queue: sqs.Queue


pipe_source = sources.KinesisSource(source_stream,
    starting_position=sources.KinesisStartingPosition.LATEST
)

pipe = pipes.Pipe(self, "Pipe",
    source=pipe_source,
    target=SqsTarget(target_queue)
)
```

### Amazon DynamoDB

A DynamoDB stream can be used as a source for a pipe. The stream will be polled for new messages and the messages will be sent to the pipe.

```python
# target_queue: sqs.Queue
table = ddb.TableV2(self, "MyTable",
    partition_key=ddb.Attribute(
        name="id",
        type=ddb.AttributeType.STRING
    ),
    dynamo_stream=ddb.StreamViewType.NEW_IMAGE
)

pipe_source = sources.DynamoDBSource(table,
    starting_position=sources.DynamoDBStartingPosition.LATEST
)

pipe = pipes.Pipe(self, "Pipe",
    source=pipe_source,
    target=SqsTarget(target_queue)
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
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_pipes_alpha as _aws_cdk_aws_pipes_alpha_c8863edb
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-sources-alpha.DynamoDBStartingPosition")
class DynamoDBStartingPosition(enum.Enum):
    '''(experimental) The position in a DynamoDB stream from which to start reading.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # target_queue: sqs.Queue
        table = ddb.TableV2(self, "MyTable",
            partition_key=ddb.Attribute(
                name="id",
                type=ddb.AttributeType.STRING
            ),
            dynamo_stream=ddb.StreamViewType.NEW_IMAGE
        )
        
        pipe_source = sources.DynamoDBSource(table,
            starting_position=sources.DynamoDBStartingPosition.LATEST
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=pipe_source,
            target=SqsTarget(target_queue)
        )
    '''

    TRIM_HORIZON = "TRIM_HORIZON"
    '''(experimental) Start reading at the last (untrimmed) stream record, which is the oldest record in the shard.

    :stability: experimental
    '''
    LATEST = "LATEST"
    '''(experimental) Start reading just after the most recent stream record in the shard, so that you always read the most recent data in the shard.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-sources-alpha.KinesisStartingPosition")
class KinesisStartingPosition(enum.Enum):
    '''(experimental) The position in a Kinesis stream from which to start reading.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_stream: kinesis.Stream
        # target_queue: sqs.Queue
        
        
        pipe_source = sources.KinesisSource(source_stream,
            starting_position=sources.KinesisStartingPosition.LATEST
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=pipe_source,
            target=SqsTarget(target_queue)
        )
    '''

    TRIM_HORIZON = "TRIM_HORIZON"
    '''(experimental) Start streaming at the last untrimmed record in the shard, which is the oldest data record in the shard.

    :stability: experimental
    '''
    LATEST = "LATEST"
    '''(experimental) Start streaming just after the most recent record in the shard, so that you always read the most recent data in the shard.

    :stability: experimental
    '''
    AT_TIMESTAMP = "AT_TIMESTAMP"
    '''(experimental) Start streaming from the position denoted by the time stamp specified in the ``startingPositionTimestamp`` field.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-sources-alpha.OnPartialBatchItemFailure")
class OnPartialBatchItemFailure(enum.Enum):
    '''(experimental) Define how to handle item process failures.

    :stability: experimental
    '''

    AUTOMATIC_BISECT = "AUTOMATIC_BISECT"
    '''(experimental) EventBridge halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch.

    :stability: experimental
    '''


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ISource)
class SqsSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.SqsSource",
):
    '''(experimental) A source that reads from an SQS queue.

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
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param queue: -
        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 10
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3784258c6cb86d0d6c344f530419061377b1cf3a2b4bd10a2a3a3d518e6645a)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        parameters = SqsSourceParameters(
            batch_size=batch_size, maximum_batching_window=maximum_batching_window
        )

        jsii.create(self.__class__, self, [queue, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.SourceConfig:
        '''(experimental) Bind the source to a pipe.

        :param _pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288529f29ea0c4faf3b003c02ed1b190d850056787292379411cafe02966c71a)
            check_type(argname="argument _pipe", value=_pipe, expected_type=type_hints["_pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.SourceConfig, jsii.invoke(self, "bind", [_pipe]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df71fa0c44f16032eebb6a467bec1301626aa930c691f81d4725ae2b34a7293d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''(experimental) The ARN of the source resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.SqsSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "batch_size": "batchSize",
        "maximum_batching_window": "maximumBatchingWindow",
    },
)
class SqsSourceParameters:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''(experimental) Parameters for the SQS source.

        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 10
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: 1

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
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc1e53379fabcd3652a828c1eb292eb8d0f78fb09fe006f68282628d259c9e2)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window", value=maximum_batching_window, expected_type=type_hints["maximum_batching_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window is not None:
            self._values["maximum_batching_window"] = maximum_batching_window

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of records to include in each batch.

        :default: 10

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcesqsqueueparameters.html#cfn-pipes-pipe-pipesourcesqsqueueparameters-batchsize
        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum length of a time to wait for events.

        :default: 1

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcesqsqueueparameters.html#cfn-pipes-pipe-pipesourcesqsqueueparameters-maximumbatchingwindowinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamSource(
    _aws_cdk_aws_pipes_alpha_c8863edb.SourceWithDeadLetterTarget,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.StreamSource",
):
    '''(experimental) Streaming sources.

    :stability: experimental
    '''

    def __init__(
        self,
        source_arn: builtins.str,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_arn: The ARN of the source resource.
        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 1
        :param dead_letter_target: (experimental) Define the target to send dead-letter queue events to. The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted. You can then resolve the issue that caused the failed invocations and replay the events at a later time. In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried. Default: - no dead-letter queue or topic
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: - the events will be handled immediately
        :param maximum_record_age: (experimental) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records. Default: -1 - EventBridge won't discard old records
        :param maximum_retry_attempts: (experimental) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source. Default: -1 - EventBridge will retry failed records until the record expires in the event source
        :param on_partial_batch_item_failure: (experimental) Define how to handle item process failures. {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch. Default: off - EventBridge will retry the entire batch
        :param parallelization_factor: (experimental) The number of batches to process concurrently from each shard. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b998fbd64ce41a171683524faf122dcab3c605fe1922565804fc238fc88c3ce)
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
        source_parameters = StreamSourceParameters(
            batch_size=batch_size,
            dead_letter_target=dead_letter_target,
            maximum_batching_window=maximum_batching_window,
            maximum_record_age=maximum_record_age,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
        )

        jsii.create(self.__class__, self, [source_arn, source_parameters])

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''(experimental) The ARN of the source resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @builtins.property
    @jsii.member(jsii_name="sourceParameters")
    def source_parameters(self) -> "StreamSourceParameters":
        '''(experimental) Base parameters for streaming sources.

        :stability: experimental
        '''
        return typing.cast("StreamSourceParameters", jsii.get(self, "sourceParameters"))


class _StreamSourceProxy(
    StreamSource,
    jsii.proxy_for(_aws_cdk_aws_pipes_alpha_c8863edb.SourceWithDeadLetterTarget), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, StreamSource).__jsii_proxy_class__ = lambda : _StreamSourceProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.StreamSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "batch_size": "batchSize",
        "dead_letter_target": "deadLetterTarget",
        "maximum_batching_window": "maximumBatchingWindow",
        "maximum_record_age": "maximumRecordAge",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
    },
)
class StreamSourceParameters:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Base parameters for streaming sources.

        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 1
        :param dead_letter_target: (experimental) Define the target to send dead-letter queue events to. The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted. You can then resolve the issue that caused the failed invocations and replay the events at a later time. In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried. Default: - no dead-letter queue or topic
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: - the events will be handled immediately
        :param maximum_record_age: (experimental) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records. Default: -1 - EventBridge won't discard old records
        :param maximum_retry_attempts: (experimental) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source. Default: -1 - EventBridge will retry failed records until the record expires in the event source
        :param on_partial_batch_item_failure: (experimental) Define how to handle item process failures. {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch. Default: off - EventBridge will retry the entire batch
        :param parallelization_factor: (experimental) The number of batches to process concurrently from each shard. Default: 1

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_pipes_sources_alpha as pipes_sources_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            
            stream_source_parameters = pipes_sources_alpha.StreamSourceParameters(
                batch_size=123,
                dead_letter_target=queue,
                maximum_batching_window=cdk.Duration.minutes(30),
                maximum_record_age=cdk.Duration.minutes(30),
                maximum_retry_attempts=123,
                on_partial_batch_item_failure=pipes_sources_alpha.OnPartialBatchItemFailure.AUTOMATIC_BISECT,
                parallelization_factor=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c656834198f37c02ad4c2b242012d534b8b501c00eeb4b79e69ee6f6146d48a7)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_target", value=dead_letter_target, expected_type=type_hints["dead_letter_target"])
            check_type(argname="argument maximum_batching_window", value=maximum_batching_window, expected_type=type_hints["maximum_batching_window"])
            check_type(argname="argument maximum_record_age", value=maximum_record_age, expected_type=type_hints["maximum_record_age"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_target is not None:
            self._values["dead_letter_target"] = dead_letter_target
        if maximum_batching_window is not None:
            self._values["maximum_batching_window"] = maximum_batching_window
        if maximum_record_age is not None:
            self._values["maximum_record_age"] = maximum_record_age
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of records to include in each batch.

        :default: 1

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-batchsize
        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]]:
        '''(experimental) Define the target to send dead-letter queue events to.

        The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted.
        You can then resolve the issue that caused the failed invocations and replay the events at a later time.
        In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried.

        :default: - no dead-letter queue or topic

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-deadletterconfig
        :stability: experimental
        '''
        result = self._values.get("dead_letter_target")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]], result)

    @builtins.property
    def maximum_batching_window(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum length of a time to wait for events.

        :default: - the events will be handled immediately

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumbatchingwindowinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def maximum_record_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Discard records older than the specified age.

        The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.

        :default: -1 - EventBridge won't discard old records

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumrecordageinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_record_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Discard records after the specified number of retries.

        The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.

        :default: -1 - EventBridge will retry failed records until the record expires in the event source

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumretryattempts
        :stability: experimental
        '''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(
        self,
    ) -> typing.Optional[OnPartialBatchItemFailure]:
        '''(experimental) Define how to handle item process failures.

        {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch.

        :default: off - EventBridge will retry the entire batch

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-onpartialbatchitemfailure
        :stability: experimental
        '''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[OnPartialBatchItemFailure], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process concurrently from each shard.

        :default: 1

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-parallelizationfactor
        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoDBSource(
    StreamSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.DynamoDBSource",
):
    '''(experimental) A source that reads from an DynamoDB stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # target_queue: sqs.Queue
        table = ddb.TableV2(self, "MyTable",
            partition_key=ddb.Attribute(
                name="id",
                type=ddb.AttributeType.STRING
            ),
            dynamo_stream=ddb.StreamViewType.NEW_IMAGE
        )
        
        pipe_source = sources.DynamoDBSource(table,
            starting_position=sources.DynamoDBStartingPosition.LATEST
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=pipe_source,
            target=SqsTarget(target_queue)
        )
    '''

    def __init__(
        self,
        table: _aws_cdk_aws_dynamodb_ceddda9d.ITableV2,
        *,
        starting_position: DynamoDBStartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param table: -
        :param starting_position: (experimental) The position in a stream from which to start reading.
        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 1
        :param dead_letter_target: (experimental) Define the target to send dead-letter queue events to. The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted. You can then resolve the issue that caused the failed invocations and replay the events at a later time. In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried. Default: - no dead-letter queue or topic
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: - the events will be handled immediately
        :param maximum_record_age: (experimental) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records. Default: -1 - EventBridge won't discard old records
        :param maximum_retry_attempts: (experimental) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source. Default: -1 - EventBridge will retry failed records until the record expires in the event source
        :param on_partial_batch_item_failure: (experimental) Define how to handle item process failures. {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch. Default: off - EventBridge will retry the entire batch
        :param parallelization_factor: (experimental) The number of batches to process concurrently from each shard. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725591432952285513fb5837b7fcfd4c1a12d9b23dc8a1a1441984ed1b948edf)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        parameters = DynamoDBSourceParameters(
            starting_position=starting_position,
            batch_size=batch_size,
            dead_letter_target=dead_letter_target,
            maximum_batching_window=maximum_batching_window,
            maximum_record_age=maximum_record_age,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
        )

        jsii.create(self.__class__, self, [table, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.SourceConfig:
        '''(experimental) Bind the source to a pipe.

        :param _pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31a4d2bb62d3b8dcbcd129bb9147b5a93cff82c68bcc95308849499fea0a35d)
            check_type(argname="argument _pipe", value=_pipe, expected_type=type_hints["_pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.SourceConfig, jsii.invoke(self, "bind", [_pipe]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2988d21015d666c7349cc7de00fd3ce7d184e8598a58f177f2a1fa7a1524d553)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.DynamoDBSourceParameters",
    jsii_struct_bases=[StreamSourceParameters],
    name_mapping={
        "batch_size": "batchSize",
        "dead_letter_target": "deadLetterTarget",
        "maximum_batching_window": "maximumBatchingWindow",
        "maximum_record_age": "maximumRecordAge",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
        "starting_position": "startingPosition",
    },
)
class DynamoDBSourceParameters(StreamSourceParameters):
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        starting_position: DynamoDBStartingPosition,
    ) -> None:
        '''(experimental) Parameters for the DynamoDB source.

        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 1
        :param dead_letter_target: (experimental) Define the target to send dead-letter queue events to. The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted. You can then resolve the issue that caused the failed invocations and replay the events at a later time. In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried. Default: - no dead-letter queue or topic
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: - the events will be handled immediately
        :param maximum_record_age: (experimental) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records. Default: -1 - EventBridge won't discard old records
        :param maximum_retry_attempts: (experimental) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source. Default: -1 - EventBridge will retry failed records until the record expires in the event source
        :param on_partial_batch_item_failure: (experimental) Define how to handle item process failures. {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch. Default: off - EventBridge will retry the entire batch
        :param parallelization_factor: (experimental) The number of batches to process concurrently from each shard. Default: 1
        :param starting_position: (experimental) The position in a stream from which to start reading.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # target_queue: sqs.Queue
            table = ddb.TableV2(self, "MyTable",
                partition_key=ddb.Attribute(
                    name="id",
                    type=ddb.AttributeType.STRING
                ),
                dynamo_stream=ddb.StreamViewType.NEW_IMAGE
            )
            
            pipe_source = sources.DynamoDBSource(table,
                starting_position=sources.DynamoDBStartingPosition.LATEST
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=pipe_source,
                target=SqsTarget(target_queue)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a027fddbf1c161997c36740761bfcd69d584d514ada94371d9e742356c091e82)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_target", value=dead_letter_target, expected_type=type_hints["dead_letter_target"])
            check_type(argname="argument maximum_batching_window", value=maximum_batching_window, expected_type=type_hints["maximum_batching_window"])
            check_type(argname="argument maximum_record_age", value=maximum_record_age, expected_type=type_hints["maximum_record_age"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_target is not None:
            self._values["dead_letter_target"] = dead_letter_target
        if maximum_batching_window is not None:
            self._values["maximum_batching_window"] = maximum_batching_window
        if maximum_record_age is not None:
            self._values["maximum_record_age"] = maximum_record_age
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of records to include in each batch.

        :default: 1

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-batchsize
        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]]:
        '''(experimental) Define the target to send dead-letter queue events to.

        The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted.
        You can then resolve the issue that caused the failed invocations and replay the events at a later time.
        In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried.

        :default: - no dead-letter queue or topic

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-deadletterconfig
        :stability: experimental
        '''
        result = self._values.get("dead_letter_target")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]], result)

    @builtins.property
    def maximum_batching_window(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum length of a time to wait for events.

        :default: - the events will be handled immediately

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumbatchingwindowinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def maximum_record_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Discard records older than the specified age.

        The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.

        :default: -1 - EventBridge won't discard old records

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumrecordageinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_record_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Discard records after the specified number of retries.

        The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.

        :default: -1 - EventBridge will retry failed records until the record expires in the event source

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumretryattempts
        :stability: experimental
        '''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(
        self,
    ) -> typing.Optional[OnPartialBatchItemFailure]:
        '''(experimental) Define how to handle item process failures.

        {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch.

        :default: off - EventBridge will retry the entire batch

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-onpartialbatchitemfailure
        :stability: experimental
        '''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[OnPartialBatchItemFailure], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process concurrently from each shard.

        :default: 1

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-parallelizationfactor
        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_position(self) -> DynamoDBStartingPosition:
        '''(experimental) The position in a stream from which to start reading.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-startingposition
        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(DynamoDBStartingPosition, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoDBSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisSource(
    StreamSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.KinesisSource",
):
    '''(experimental) A source that reads from Kinesis.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_stream: kinesis.Stream
        # target_queue: sqs.Queue
        
        
        pipe_source = sources.KinesisSource(source_stream,
            starting_position=sources.KinesisStartingPosition.LATEST
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=pipe_source,
            target=SqsTarget(target_queue)
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
        *,
        starting_position: KinesisStartingPosition,
        starting_position_timestamp: typing.Optional[datetime.datetime] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param stream: -
        :param starting_position: (experimental) The position in a stream from which to start reading.
        :param starting_position_timestamp: (experimental) With StartingPosition set to AT_TIMESTAMP, the time from which to start reading, in ISO 8601 format. Default: - no starting position timestamp
        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 1
        :param dead_letter_target: (experimental) Define the target to send dead-letter queue events to. The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted. You can then resolve the issue that caused the failed invocations and replay the events at a later time. In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried. Default: - no dead-letter queue or topic
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: - the events will be handled immediately
        :param maximum_record_age: (experimental) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records. Default: -1 - EventBridge won't discard old records
        :param maximum_retry_attempts: (experimental) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source. Default: -1 - EventBridge will retry failed records until the record expires in the event source
        :param on_partial_batch_item_failure: (experimental) Define how to handle item process failures. {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch. Default: off - EventBridge will retry the entire batch
        :param parallelization_factor: (experimental) The number of batches to process concurrently from each shard. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f9b8e63bc51294afb43ead5f02fe4af4ccd960baa18cf0420a28658abfeef3)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        parameters = KinesisSourceParameters(
            starting_position=starting_position,
            starting_position_timestamp=starting_position_timestamp,
            batch_size=batch_size,
            dead_letter_target=dead_letter_target,
            maximum_batching_window=maximum_batching_window,
            maximum_record_age=maximum_record_age,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
        )

        jsii.create(self.__class__, self, [stream, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.SourceConfig:
        '''(experimental) Bind the source to a pipe.

        :param _pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bb7b50075cc2120fa88cb9a80b9aad7d1ca756d4e050e2ec5698f58156591c)
            check_type(argname="argument _pipe", value=_pipe, expected_type=type_hints["_pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.SourceConfig, jsii.invoke(self, "bind", [_pipe]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role read access to the source.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e5c29ad7c6f6f50c42c0789bd03bec04b2329d892005b6abc80fa4ac28f75d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-sources-alpha.KinesisSourceParameters",
    jsii_struct_bases=[StreamSourceParameters],
    name_mapping={
        "batch_size": "batchSize",
        "dead_letter_target": "deadLetterTarget",
        "maximum_batching_window": "maximumBatchingWindow",
        "maximum_record_age": "maximumRecordAge",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
        "starting_position": "startingPosition",
        "starting_position_timestamp": "startingPositionTimestamp",
    },
)
class KinesisSourceParameters(StreamSourceParameters):
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
        maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        starting_position: KinesisStartingPosition,
        starting_position_timestamp: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''(experimental) Parameters for the Kinesis source.

        :param batch_size: (experimental) The maximum number of records to include in each batch. Default: 1
        :param dead_letter_target: (experimental) Define the target to send dead-letter queue events to. The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted. You can then resolve the issue that caused the failed invocations and replay the events at a later time. In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried. Default: - no dead-letter queue or topic
        :param maximum_batching_window: (experimental) The maximum length of a time to wait for events. Default: - the events will be handled immediately
        :param maximum_record_age: (experimental) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records. Default: -1 - EventBridge won't discard old records
        :param maximum_retry_attempts: (experimental) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source. Default: -1 - EventBridge will retry failed records until the record expires in the event source
        :param on_partial_batch_item_failure: (experimental) Define how to handle item process failures. {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch. Default: off - EventBridge will retry the entire batch
        :param parallelization_factor: (experimental) The number of batches to process concurrently from each shard. Default: 1
        :param starting_position: (experimental) The position in a stream from which to start reading.
        :param starting_position_timestamp: (experimental) With StartingPosition set to AT_TIMESTAMP, the time from which to start reading, in ISO 8601 format. Default: - no starting position timestamp

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_stream: kinesis.Stream
            # target_queue: sqs.Queue
            
            
            pipe_source = sources.KinesisSource(source_stream,
                starting_position=sources.KinesisStartingPosition.LATEST
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=pipe_source,
                target=SqsTarget(target_queue)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175577b4da2d18db2b09cfe8c472e1e61fcc027f61613267ec6aeb6417213054)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_target", value=dead_letter_target, expected_type=type_hints["dead_letter_target"])
            check_type(argname="argument maximum_batching_window", value=maximum_batching_window, expected_type=type_hints["maximum_batching_window"])
            check_type(argname="argument maximum_record_age", value=maximum_record_age, expected_type=type_hints["maximum_record_age"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_target is not None:
            self._values["dead_letter_target"] = dead_letter_target
        if maximum_batching_window is not None:
            self._values["maximum_batching_window"] = maximum_batching_window
        if maximum_record_age is not None:
            self._values["maximum_record_age"] = maximum_record_age
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of records to include in each batch.

        :default: 1

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-batchsize
        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]]:
        '''(experimental) Define the target to send dead-letter queue events to.

        The dead-letter queue stores any events that are not successfully delivered to a Pipes target after all retry attempts are exhausted.
        You can then resolve the issue that caused the failed invocations and replay the events at a later time.
        In some cases, such as when access is denied to a resource, events are sent directly to the dead-letter queue and are not retried.

        :default: - no dead-letter queue or topic

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-deadletterconfig
        :stability: experimental
        '''
        result = self._values.get("dead_letter_target")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]], result)

    @builtins.property
    def maximum_batching_window(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum length of a time to wait for events.

        :default: - the events will be handled immediately

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumbatchingwindowinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def maximum_record_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Discard records older than the specified age.

        The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.

        :default: -1 - EventBridge won't discard old records

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumrecordageinseconds
        :stability: experimental
        '''
        result = self._values.get("maximum_record_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Discard records after the specified number of retries.

        The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.

        :default: -1 - EventBridge will retry failed records until the record expires in the event source

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumretryattempts
        :stability: experimental
        '''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(
        self,
    ) -> typing.Optional[OnPartialBatchItemFailure]:
        '''(experimental) Define how to handle item process failures.

        {@link OnPartialBatchItemFailure.AUTOMATIC_BISECT} halves each batch and will retry each half until all the records are processed or there is one failed message left in the batch.

        :default: off - EventBridge will retry the entire batch

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-onpartialbatchitemfailure
        :stability: experimental
        '''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[OnPartialBatchItemFailure], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process concurrently from each shard.

        :default: 1

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-parallelizationfactor
        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_position(self) -> KinesisStartingPosition:
        '''(experimental) The position in a stream from which to start reading.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-startingposition
        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(KinesisStartingPosition, result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[datetime.datetime]:
        '''(experimental) With StartingPosition set to AT_TIMESTAMP, the time from which to start reading, in ISO 8601 format.

        :default: - no starting position timestamp

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-startingpositiontimestamp
        :stability: experimental

        Example::

            Date(Date.UTC(1969, 10, 20, 0, 0, 0))
        '''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DynamoDBSource",
    "DynamoDBSourceParameters",
    "DynamoDBStartingPosition",
    "KinesisSource",
    "KinesisSourceParameters",
    "KinesisStartingPosition",
    "OnPartialBatchItemFailure",
    "SqsSource",
    "SqsSourceParameters",
    "StreamSource",
    "StreamSourceParameters",
]

publication.publish()

def _typecheckingstub__a3784258c6cb86d0d6c344f530419061377b1cf3a2b4bd10a2a3a3d518e6645a(
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288529f29ea0c4faf3b003c02ed1b190d850056787292379411cafe02966c71a(
    _pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df71fa0c44f16032eebb6a467bec1301626aa930c691f81d4725ae2b34a7293d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc1e53379fabcd3652a828c1eb292eb8d0f78fb09fe006f68282628d259c9e2(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b998fbd64ce41a171683524faf122dcab3c605fe1922565804fc238fc88c3ce(
    source_arn: builtins.str,
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c656834198f37c02ad4c2b242012d534b8b501c00eeb4b79e69ee6f6146d48a7(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725591432952285513fb5837b7fcfd4c1a12d9b23dc8a1a1441984ed1b948edf(
    table: _aws_cdk_aws_dynamodb_ceddda9d.ITableV2,
    *,
    starting_position: DynamoDBStartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31a4d2bb62d3b8dcbcd129bb9147b5a93cff82c68bcc95308849499fea0a35d(
    _pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2988d21015d666c7349cc7de00fd3ce7d184e8598a58f177f2a1fa7a1524d553(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a027fddbf1c161997c36740761bfcd69d584d514ada94371d9e742356c091e82(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position: DynamoDBStartingPosition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f9b8e63bc51294afb43ead5f02fe4af4ccd960baa18cf0420a28658abfeef3(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
    *,
    starting_position: KinesisStartingPosition,
    starting_position_timestamp: typing.Optional[datetime.datetime] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bb7b50075cc2120fa88cb9a80b9aad7d1ca756d4e050e2ec5698f58156591c(
    _pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e5c29ad7c6f6f50c42c0789bd03bec04b2329d892005b6abc80fa4ac28f75d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175577b4da2d18db2b09cfe8c472e1e61fcc027f61613267ec6aeb6417213054(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_target: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.IQueue, _aws_cdk_aws_sns_ceddda9d.ITopic]] = None,
    maximum_batching_window: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_record_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[OnPartialBatchItemFailure] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position: KinesisStartingPosition,
    starting_position_timestamp: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass
