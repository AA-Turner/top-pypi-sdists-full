'''
# AWS Lambda Event Sources

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

An event source mapping is an AWS Lambda resource that reads from an event source and invokes a Lambda function.
You can use event source mappings to process items from a stream or queue in services that don't invoke Lambda
functions directly. Lambda provides event source mappings for the following services. Read more about lambda
event sources [here](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html).

This module includes classes that allow using various AWS services as event
sources for AWS Lambda via the high-level `lambda.addEventSource(source)` API.

NOTE: In most cases, it is also possible to use the resource APIs to invoke an
AWS Lambda function. This library provides a uniform API for all Lambda event
sources regardless of the underlying mechanism they use.

The following code sets up a lambda function with an SQS queue event source -

```python
from aws_cdk.aws_lambda_event_sources import SqsEventSource

# fn: lambda.Function

queue = sqs.Queue(self, "MyQueue")
event_source = SqsEventSource(queue)
fn.add_event_source(event_source)

event_source_id = event_source.event_source_mapping_id
```

The `eventSourceId` property contains the event source id. This will be a
[token](https://docs.aws.amazon.com/cdk/latest/guide/tokens.html) that will resolve to the final value at the time of
deployment.

## SQS

Amazon Simple Queue Service (Amazon SQS) allows you to build asynchronous
workflows. For more information about Amazon SQS, see Amazon Simple Queue
Service. You can configure AWS Lambda to poll for these messages as they arrive
and then pass the event to a Lambda function invocation. To view a sample event,
see [Amazon SQS Event](https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-sqs).

To set up Amazon Simple Queue Service as an event source for AWS Lambda, you
first create or update an Amazon SQS queue and select custom values for the
queue parameters. The following parameters will impact Amazon SQS's polling
behavior:

* **visibilityTimeout**: May impact the period between retries.
* **receiveMessageWaitTime**: Will determine [long
  poll](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-long-polling.html)
  duration. The default value is 20 seconds.
* **batchSize**: Determines how many records are buffered before invoking your lambda function.
* **maxBatchingWindow**: The maximum amount of time to gather records before invoking the lambda. This increases the likelihood of a full batch at the cost of delayed processing.
* **enabled**: If the SQS event source mapping should be enabled. The default is true.

```python
from aws_cdk.aws_lambda_event_sources import SqsEventSource
# fn: lambda.Function


queue = sqs.Queue(self, "MyQueue",
    visibility_timeout=Duration.seconds(30),  # default,
    receive_message_wait_time=Duration.seconds(20)
)

fn.add_event_source(SqsEventSource(queue,
    batch_size=10,  # default
    max_batching_window=Duration.minutes(5),
    report_batch_item_failures=True
))
```

## S3

You can write Lambda functions to process S3 bucket events, such as the
object-created or object-deleted events. For example, when a user uploads a
photo to a bucket, you might want Amazon S3 to invoke your Lambda function so
that it reads the image and creates a thumbnail for the photo.

You can use the bucket notification configuration feature in Amazon S3 to
configure the event source mapping, identifying the bucket events that you want
Amazon S3 to publish and which Lambda function to invoke.

```python
import aws_cdk.aws_s3 as s3
from aws_cdk.aws_lambda_event_sources import S3EventSource
# fn: lambda.Function


bucket = s3.Bucket(self, "mybucket")

fn.add_event_source(S3EventSource(bucket,
    events=[s3.EventType.OBJECT_CREATED, s3.EventType.OBJECT_REMOVED],
    filters=[s3.NotificationKeyFilter(prefix="subdir/")]
))
```

## SNS

You can write Lambda functions to process Amazon Simple Notification Service
notifications. When a message is published to an Amazon SNS topic, the service
can invoke your Lambda function by passing the message payload as a parameter.
Your Lambda function code can then process the event, for example publish the
message to other Amazon SNS topics, or send the message to other AWS services.

This also enables you to trigger a Lambda function in response to Amazon
CloudWatch alarms and other AWS services that use Amazon SNS.

For an example event, see [Appendix: Message and JSON
Formats](https://docs.aws.amazon.com/sns/latest/dg/json-formats.html) and
[Amazon SNS Sample
Event](https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-sns).
For an example use case, see [Using AWS Lambda with Amazon SNS from Different
Accounts](https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html).

```python
import aws_cdk.aws_sns as sns
from aws_cdk.aws_lambda_event_sources import SnsEventSource

# topic: sns.Topic

# fn: lambda.Function

dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
fn.add_event_source(SnsEventSource(topic,
    filter_policy={},
    dead_letter_queue=dead_letter_queue
))
```

When a user calls the SNS Publish API on a topic that your Lambda function is
subscribed to, Amazon SNS will call Lambda to invoke your function
asynchronously. Lambda will then return a delivery status. If there was an error
calling Lambda, Amazon SNS will retry invoking the Lambda function up to three
times. After three tries, if Amazon SNS still could not successfully invoke the
Lambda function, then Amazon SNS will send a delivery status failure message to
CloudWatch.

## DynamoDB Streams

You can write Lambda functions to process change events from a DynamoDB Table. An event is emitted to a DynamoDB stream (if configured) whenever a write (Put, Delete, Update)
operation is performed against the table. See [Using AWS Lambda with Amazon DynamoDB](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html) for more information about configuring Lambda function event sources with DynamoDB.

To process events with a Lambda function, first create or update a DynamoDB table and enable a `stream` specification. Then, create a `DynamoEventSource`
and add it to your Lambda function. The following parameters will impact Amazon DynamoDB's polling behavior:

* **batchSize**: Determines how many records are buffered before invoking your lambda function - could impact your function's memory usage (if too high) and ability to keep up with incoming data velocity (if too low).
* **bisectBatchOnError**: If a batch encounters an error, this will cause the batch to be split in two and have each new smaller batch retried, allowing the records in error to be isolated.
* **reportBatchItemFailures**: Allow functions to return partially successful responses for a batch of records.
* **maxBatchingWindow**: The maximum amount of time to gather records before invoking the lambda. This increases the likelihood of a full batch at the cost of delayed processing.
* **maxRecordAge**: The maximum age of a record that will be sent to the function for processing. Records that exceed the max age will be treated as failures.
* **onFailure**: In the event a record fails after all retries or if the record age has exceeded the configured value, the record will be sent to SQS queue or SNS topic that is specified here
* **parallelizationFactor**: The number of batches to concurrently process on each shard.
* **retryAttempts**: The maximum number of times a record should be retried in the event of failure.
* **startingPosition**: Will determine where to being consumption, either at the most recent ('LATEST') record or the oldest record ('TRIM_HORIZON'). 'TRIM_HORIZON' will ensure you process all available data, while 'LATEST' will ignore all records that arrived prior to attaching the event source.
* **tumblingWindow**: The duration in seconds of a processing window when using streams.
* **enabled**: If the DynamoDB Streams event source mapping should be enabled. The default is true.

```python
import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq

# table: dynamodb.Table

# fn: lambda.Function


dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
fn.add_event_source(DynamoEventSource(table,
    starting_position=lambda_.StartingPosition.TRIM_HORIZON,
    batch_size=5,
    bisect_batch_on_error=True,
    on_failure=SqsDlq(dead_letter_queue),
    retry_attempts=10
))
```

## Kinesis

You can write Lambda functions to process streaming data in Amazon Kinesis Streams. For more information about Amazon Kinesis, see [Amazon Kinesis
Service](https://aws.amazon.com/kinesis/data-streams/). To learn more about configuring Lambda function event sources with kinesis and view a sample event,
see [Amazon Kinesis Event](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html).

To set up Amazon Kinesis as an event source for AWS Lambda, you
first create or update an Amazon Kinesis stream and select custom values for the
event source parameters. The following parameters will impact Amazon Kinesis's polling
behavior:

* **batchSize**: Determines how many records are buffered before invoking your lambda function - could impact your function's memory usage (if too high) and ability to keep up with incoming data velocity (if too low).
* **bisectBatchOnError**: If a batch encounters an error, this will cause the batch to be split in two and have each new smaller batch retried, allowing the records in error to be isolated.
* **reportBatchItemFailures**: Allow functions to return partially successful responses for a batch of records.
* **maxBatchingWindow**: The maximum amount of time to gather records before invoking the lambda. This increases the likelihood of a full batch at the cost of possibly delaying processing.
* **maxRecordAge**: The maximum age of a record that will be sent to the function for processing. Records that exceed the max age will be treated as failures.
* **onFailure**: In the event a record fails and consumes all retries, the record will be sent to SQS queue or SNS topic that is specified here
* **parallelizationFactor**: The number of batches to concurrently process on each shard.
* **retryAttempts**: The maximum number of times a record should be retried in the event of failure.
* **startingPosition**: Will determine where to being consumption, either at the most recent ('LATEST') record or the oldest record ('TRIM_HORIZON'). 'TRIM_HORIZON' will ensure you process all available data, while 'LATEST' will ignore all records that arrived prior to attaching the event source.
* **tumblingWindow**: The duration in seconds of a processing window when using streams.
* **enabled**: If the DynamoDB Streams event source mapping should be enabled. The default is true.

```python
import aws_cdk.aws_kinesis as kinesis
from aws_cdk.aws_lambda_event_sources import KinesisEventSource

# my_function: lambda.Function


stream = kinesis.Stream(self, "MyStream")
my_function.add_event_source(KinesisEventSource(stream,
    batch_size=100,  # default
    starting_position=lambda_.StartingPosition.TRIM_HORIZON
))
```

## Kafka

You can write Lambda functions to process data either from [Amazon MSK](https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html) or a [self managed Kafka](https://docs.aws.amazon.com/lambda/latest/dg/kafka-smaa.html) cluster.

The following code sets up Amazon MSK as an event source for a lambda function. Credentials will need to be configured to access the
MSK cluster, as described in [Username/Password authentication](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html).

```python
from aws_cdk.aws_secretsmanager import Secret
from aws_cdk.aws_lambda_event_sources import ManagedKafkaEventSource

# my_function: lambda.Function


# Your MSK cluster arn
cluster_arn = "arn:aws:kafka:us-east-1:0123456789019:cluster/SalesCluster/abcd1234-abcd-cafe-abab-9876543210ab-4"

# The Kafka topic you want to subscribe to
topic = "some-cool-topic"

# The secret that allows access to your MSK cluster
# You still have to make sure that it is associated with your cluster as described in the documentation
secret = Secret(self, "Secret", secret_name="AmazonMSK_KafkaSecret")
my_function.add_event_source(ManagedKafkaEventSource(
    cluster_arn=cluster_arn,
    topic=topic,
    secret=secret,
    batch_size=100,  # default
    starting_position=lambda_.StartingPosition.TRIM_HORIZON
))
```

The following code sets up a self managed Kafka cluster as an event source. Username and password based authentication
will need to be set up as described in [Managing access and permissions](https://docs.aws.amazon.com/lambda/latest/dg/smaa-permissions.html#smaa-permissions-add-secret).

```python
from aws_cdk.aws_secretsmanager import Secret
from aws_cdk.aws_lambda_event_sources import SelfManagedKafkaEventSource

# The secret that allows access to your self hosted Kafka cluster
# secret: Secret

# my_function: lambda.Function


# The list of Kafka brokers
bootstrap_servers = ["kafka-broker:9092"]

# The Kafka topic you want to subscribe to
topic = "some-cool-topic"
my_function.add_event_source(SelfManagedKafkaEventSource(
    bootstrap_servers=bootstrap_servers,
    topic=topic,
    secret=secret,
    batch_size=100,  # default
    starting_position=lambda_.StartingPosition.TRIM_HORIZON
))
```

If your self managed Kafka cluster is only reachable via VPC also configure `vpc` `vpcSubnets` and `securityGroup`.

## Roadmap

Eventually, this module will support all the event sources described under
[Supported Event
Sources](https://docs.aws.amazon.com/lambda/latest/dg/invoking-lambda-function.html)
in the AWS Lambda Developer Guide.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_f01c2838
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_eb1dc53b
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_0674c215
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_72af8d6f
import aws_cdk.aws_sns as _aws_cdk_aws_sns_889c7272
import aws_cdk.aws_sns_subscriptions as _aws_cdk_aws_sns_subscriptions_d19397b0
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_48bffef9
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSource)
class ApiEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.ApiEventSource",
):
    '''
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigateway as apigateway
        import aws_cdk.aws_lambda_event_sources as lambda_event_sources
        
        # authorizer: apigateway.Authorizer
        # model: apigateway.Model
        # request_validator: apigateway.RequestValidator
        
        api_event_source = lambda_event_sources.ApiEventSource("method", "path",
            api_key_required=False,
            authorization_scopes=["authorizationScopes"],
            authorization_type=apigateway.AuthorizationType.NONE,
            authorizer=authorizer,
            method_responses=[apigateway.MethodResponse(
                status_code="statusCode",
        
                # the properties below are optional
                response_models={
                    "response_models_key": model
                },
                response_parameters={
                    "response_parameters_key": False
                }
            )],
            operation_name="operationName",
            request_models={
                "request_models_key": model
            },
            request_parameters={
                "request_parameters_key": False
            },
            request_validator=request_validator,
            request_validator_options=apigateway.RequestValidatorOptions(
                request_validator_name="requestValidatorName",
                validate_request_body=False,
                validate_request_parameters=False
            )
        )
    '''

    def __init__(
        self,
        method: builtins.str,
        path: builtins.str,
        *,
        api_key_required: typing.Optional[builtins.bool] = None,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorization_type: typing.Optional[_aws_cdk_aws_apigateway_f01c2838.AuthorizationType] = None,
        authorizer: typing.Optional[_aws_cdk_aws_apigateway_f01c2838.IAuthorizer] = None,
        method_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_apigateway_f01c2838.MethodResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_apigateway_f01c2838.IModel]] = None,
        request_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        request_validator: typing.Optional[_aws_cdk_aws_apigateway_f01c2838.IRequestValidator] = None,
        request_validator_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_f01c2838.RequestValidatorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param method: -
        :param path: -
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_scopes: A list of authorization scopes configured on the method. The scopes are used with a COGNITO_USER_POOLS authorizer to authorize the method invocation. Default: - no authorization scopes
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The models which describe data structure of request payload. When combined with ``requestValidator`` or ``requestValidatorOptions``, the service will validate the API request payload before it reaches the API's Integration (including proxies). Specify ``requestModels`` as key-value pairs, with a content type (e.g. ``'application/json'``) as the key and an API Gateway Model as the value.
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator. Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator
        :param request_validator_options: Request validator options to create new validator Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076fcd6efcc0dd0bc285557ce6dae238e8c87390924592dee0eab5aaad98924d)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _aws_cdk_aws_apigateway_f01c2838.MethodOptions(
            api_key_required=api_key_required,
            authorization_scopes=authorization_scopes,
            authorization_type=authorization_type,
            authorizer=authorizer,
            method_responses=method_responses,
            operation_name=operation_name,
            request_models=request_models,
            request_parameters=request_parameters,
            request_validator=request_validator,
            request_validator_options=request_validator_options,
        )

        jsii.create(self.__class__, self, [method, path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffd76e94c35b3440c6f6fc5714a9d3141b8269baf677e4a5cc6d37864f51785)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))


@jsii.enum(jsii_type="@aws-cdk/aws-lambda-event-sources.AuthenticationMethod")
class AuthenticationMethod(enum.Enum):
    '''The authentication method to use with SelfManagedKafkaEventSource.'''

    SASL_SCRAM_512_AUTH = "SASL_SCRAM_512_AUTH"
    '''SASL_SCRAM_512_AUTH authentication method for your Kafka cluster.'''
    SASL_SCRAM_256_AUTH = "SASL_SCRAM_256_AUTH"
    '''SASL_SCRAM_256_AUTH authentication method for your Kafka cluster.'''
    BASIC_AUTH = "BASIC_AUTH"
    '''BASIC_AUTH (SASL/PLAIN) authentication method for your Kafka cluster.'''
    CLIENT_CERTIFICATE_TLS_AUTH = "CLIENT_CERTIFICATE_TLS_AUTH"
    '''CLIENT_CERTIFICATE_TLS_AUTH (mTLS) authentication method for your Kafka cluster.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.BaseStreamEventSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
    },
)
class BaseStreamEventSourceProps:
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''The set of properties for streaming event sources shared by Dynamo, Kinesis and Kafka.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lambda as lambda_
            import aws_cdk.aws_lambda_event_sources as lambda_event_sources
            import aws_cdk.core as cdk
            
            base_stream_event_source_props = lambda_event_sources.BaseStreamEventSourceProps(
                starting_position=lambda_.StartingPosition.TRIM_HORIZON,
            
                # the properties below are optional
                batch_size=123,
                enabled=False,
                max_batching_window=cdk.Duration.minutes(30)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6201a0056cd0f4ae8898f3c5ccda730f6c900993ff3bab23833f6e7c4d23b3)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseStreamEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.KafkaEventSourceProps",
    jsii_struct_bases=[BaseStreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "topic": "topic",
        "secret": "secret",
    },
)
class KafkaEventSourceProps(BaseStreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        topic: builtins.str,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
    ) -> None:
        '''Properties for a Kafka event source.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param topic: The Kafka topic to subscribe to.
        :param secret: The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet. Default: none

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lambda as lambda_
            import aws_cdk.aws_lambda_event_sources as lambda_event_sources
            import aws_cdk.aws_secretsmanager as secretsmanager
            import aws_cdk.core as cdk
            
            # secret: secretsmanager.Secret
            
            kafka_event_source_props = lambda_event_sources.KafkaEventSourceProps(
                starting_position=lambda_.StartingPosition.TRIM_HORIZON,
                topic="topic",
            
                # the properties below are optional
                batch_size=123,
                enabled=False,
                max_batching_window=cdk.Duration.minutes(30),
                secret=secret
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e338a5a9e12b0674a4526b98f0e26b09ec5225de9b9e9ce6996864d9c86eef)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
            "topic": topic,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''The Kafka topic to subscribe to.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret]:
        '''The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet.

        :default: none
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KafkaEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.ManagedKafkaEventSourceProps",
    jsii_struct_bases=[KafkaEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "topic": "topic",
        "secret": "secret",
        "cluster_arn": "clusterArn",
    },
)
class ManagedKafkaEventSourceProps(KafkaEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        topic: builtins.str,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
        cluster_arn: builtins.str,
    ) -> None:
        '''Properties for a MSK event source.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param topic: The Kafka topic to subscribe to.
        :param secret: The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet. Default: none
        :param cluster_arn: An MSK cluster construct.

        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_secretsmanager import Secret
            from aws_cdk.aws_lambda_event_sources import ManagedKafkaEventSource
            
            # my_function: lambda.Function
            
            
            # Your MSK cluster arn
            cluster_arn = "arn:aws:kafka:us-east-1:0123456789019:cluster/SalesCluster/abcd1234-abcd-cafe-abab-9876543210ab-4"
            
            # The Kafka topic you want to subscribe to
            topic = "some-cool-topic"
            
            # The secret that allows access to your MSK cluster
            # You still have to make sure that it is associated with your cluster as described in the documentation
            secret = Secret(self, "Secret", secret_name="AmazonMSK_KafkaSecret")
            my_function.add_event_source(ManagedKafkaEventSource(
                cluster_arn=cluster_arn,
                topic=topic,
                secret=secret,
                batch_size=100,  # default
                starting_position=lambda_.StartingPosition.TRIM_HORIZON
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a85299498386cebec70e76d822d45da40b4ce5130174d9873a4ee5b7d0db1f1)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
            "topic": topic,
            "cluster_arn": cluster_arn,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''The Kafka topic to subscribe to.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret]:
        '''The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet.

        :default: none
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret], result)

    @builtins.property
    def cluster_arn(self) -> builtins.str:
        '''An MSK cluster construct.'''
        result = self._values.get("cluster_arn")
        assert result is not None, "Required property 'cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSource)
class S3EventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.S3EventSource",
):
    '''Use S3 bucket notifications as an event source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_lambda_event_sources as eventsources
        import aws_cdk.aws_s3 as s3
        
        # fn: lambda.Function
        
        bucket = s3.Bucket(self, "Bucket")
        fn.add_event_source(eventsources.S3EventSource(bucket,
            events=[s3.EventType.OBJECT_CREATED, s3.EventType.OBJECT_REMOVED],
            filters=[s3.NotificationKeyFilter(prefix="subdir/")]
        ))
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_55f001a5.Bucket,
        *,
        events: typing.Sequence[_aws_cdk_aws_s3_55f001a5.EventType],
        filters: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_55f001a5.NotificationKeyFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param bucket: -
        :param events: The s3 event types that will trigger the notification.
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9121bfbc3d21f50d01f9fb8c97b399a92c4e02e9e60d33ba4d314c7f3c13b9)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        props = S3EventSourceProps(events=events, filters=filters)

        jsii.create(self.__class__, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3eac6618bf058611b96de1366ce6807d697e843d3fff793fc5bae142eada82)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_55f001a5.Bucket:
        return typing.cast(_aws_cdk_aws_s3_55f001a5.Bucket, jsii.get(self, "bucket"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.S3EventSourceProps",
    jsii_struct_bases=[],
    name_mapping={"events": "events", "filters": "filters"},
)
class S3EventSourceProps:
    def __init__(
        self,
        *,
        events: typing.Sequence[_aws_cdk_aws_s3_55f001a5.EventType],
        filters: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_55f001a5.NotificationKeyFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param events: The s3 event types that will trigger the notification.
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_lambda_event_sources as eventsources
            import aws_cdk.aws_s3 as s3
            
            # fn: lambda.Function
            
            bucket = s3.Bucket(self, "Bucket")
            fn.add_event_source(eventsources.S3EventSource(bucket,
                events=[s3.EventType.OBJECT_CREATED, s3.EventType.OBJECT_REMOVED],
                filters=[s3.NotificationKeyFilter(prefix="subdir/")]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31c9a2adefdac1f8e285d3d2f83d6c23a006a88c833b5d1bc521f576579bd85)
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "events": events,
        }
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def events(self) -> typing.List[_aws_cdk_aws_s3_55f001a5.EventType]:
        '''The s3 event types that will trigger the notification.'''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_s3_55f001a5.EventType], result)

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_55f001a5.NotificationKeyFilter]]:
        '''S3 object key filter rules to determine which objects trigger this event.

        Each filter must include a ``prefix`` and/or ``suffix`` that will be matched
        against the s3 object key. Refer to the S3 Developer Guide for details
        about allowed filter rules.
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_55f001a5.NotificationKeyFilter]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3EventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.SelfManagedKafkaEventSourceProps",
    jsii_struct_bases=[KafkaEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "topic": "topic",
        "secret": "secret",
        "bootstrap_servers": "bootstrapServers",
        "authentication_method": "authenticationMethod",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SelfManagedKafkaEventSourceProps(KafkaEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        topic: builtins.str,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
        bootstrap_servers: typing.Sequence[builtins.str],
        authentication_method: typing.Optional[AuthenticationMethod] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for a self managed Kafka cluster event source.

        If your Kafka cluster is only reachable via VPC make sure to configure it.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param topic: The Kafka topic to subscribe to.
        :param secret: The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet. Default: none
        :param bootstrap_servers: The list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.xyz.com:xxxx``.
        :param authentication_method: The authentication method for your Kafka cluster. Default: AuthenticationMethod.SASL_SCRAM_512_AUTH
        :param security_group: If your Kafka brokers are only reachable via VPC, provide the security group here. Default: - none, required if setting vpc
        :param vpc: If your Kafka brokers are only reachable via VPC provide the VPC here. Default: none
        :param vpc_subnets: If your Kafka brokers are only reachable via VPC, provide the subnets selection here. Default: - none, required if setting vpc

        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_secretsmanager import Secret
            from aws_cdk.aws_lambda_event_sources import SelfManagedKafkaEventSource
            
            # The secret that allows access to your self hosted Kafka cluster
            # secret: Secret
            
            # my_function: lambda.Function
            
            
            # The list of Kafka brokers
            bootstrap_servers = ["kafka-broker:9092"]
            
            # The Kafka topic you want to subscribe to
            topic = "some-cool-topic"
            my_function.add_event_source(SelfManagedKafkaEventSource(
                bootstrap_servers=bootstrap_servers,
                topic=topic,
                secret=secret,
                batch_size=100,  # default
                starting_position=lambda_.StartingPosition.TRIM_HORIZON
            ))
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1da8aa7b61f62af23564d90cb79cb69ca13a3ec6d4c3bc3090291639a8cce3)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument bootstrap_servers", value=bootstrap_servers, expected_type=type_hints["bootstrap_servers"])
            check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
            "topic": topic,
            "bootstrap_servers": bootstrap_servers,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if secret is not None:
            self._values["secret"] = secret
        if authentication_method is not None:
            self._values["authentication_method"] = authentication_method
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''The Kafka topic to subscribe to.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret]:
        '''The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet.

        :default: none
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret], result)

    @builtins.property
    def bootstrap_servers(self) -> typing.List[builtins.str]:
        '''The list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself.

        They are in the format ``abc.xyz.com:xxxx``.
        '''
        result = self._values.get("bootstrap_servers")
        assert result is not None, "Required property 'bootstrap_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def authentication_method(self) -> typing.Optional[AuthenticationMethod]:
        '''The authentication method for your Kafka cluster.

        :default: AuthenticationMethod.SASL_SCRAM_512_AUTH
        '''
        result = self._values.get("authentication_method")
        return typing.cast(typing.Optional[AuthenticationMethod], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]:
        '''If your Kafka brokers are only reachable via VPC, provide the security group here.

        :default: - none, required if setting vpc
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''If your Kafka brokers are only reachable via VPC provide the VPC here.

        :default: none
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''If your Kafka brokers are only reachable via VPC, provide the subnets selection here.

        :default: - none, required if setting vpc
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelfManagedKafkaEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq)
class SnsDlq(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.SnsDlq",
):
    '''An SNS dead letter queue destination configuration for a Lambda event source.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_lambda_event_sources as lambda_event_sources
        import aws_cdk.aws_sns as sns
        
        # topic: sns.Topic
        
        sns_dlq = lambda_event_sources.SnsDlq(topic)
    '''

    def __init__(self, topic: _aws_cdk_aws_sns_889c7272.ITopic) -> None:
        '''
        :param topic: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb126758e67d5dff286cacb1de18f6b4f622b879194a6ef539ef65992547a9b0)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _target: _aws_cdk_aws_lambda_5443dbc3.IEventSourceMapping,
        target_handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    ) -> _aws_cdk_aws_lambda_5443dbc3.DlqDestinationConfig:
        '''Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a91847c9aa40be3b667209eb1fc27528e8bdf0e9a71701b0cd8bfdde1ce57d)
            check_type(argname="argument _target", value=_target, expected_type=type_hints["_target"])
            check_type(argname="argument target_handler", value=target_handler, expected_type=type_hints["target_handler"])
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.DlqDestinationConfig, jsii.invoke(self, "bind", [_target, target_handler]))


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSource)
class SnsEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.SnsEventSource",
):
    '''Use an Amazon SNS topic as an event source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        from aws_cdk.aws_lambda_event_sources import SnsEventSource
        
        # topic: sns.Topic
        
        # fn: lambda.Function
        
        dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
        fn.add_event_source(SnsEventSource(topic,
            filter_policy={},
            dead_letter_queue=dead_letter_queue
        ))
    '''

    def __init__(
        self,
        topic: _aws_cdk_aws_sns_889c7272.ITopic,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_sns_889c7272.SubscriptionFilter]] = None,
    ) -> None:
        '''
        :param topic: -
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fe301a5781e6d4e8b042935df62070f7b9868b7fbb5c96150f76b4bf4f8397)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = SnsEventSourceProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(self.__class__, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3a63957448746235ed395874f9f97dacb0123e4be255920814c1434ace9b7b)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> _aws_cdk_aws_sns_889c7272.ITopic:
        return typing.cast(_aws_cdk_aws_sns_889c7272.ITopic, jsii.get(self, "topic"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.SnsEventSourceProps",
    jsii_struct_bases=[
        _aws_cdk_aws_sns_subscriptions_d19397b0.LambdaSubscriptionProps
    ],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SnsEventSourceProps(
    _aws_cdk_aws_sns_subscriptions_d19397b0.LambdaSubscriptionProps,
):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_sns_889c7272.SubscriptionFilter]] = None,
    ) -> None:
        '''Properties forwarded to the Lambda Subscription.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sns as sns
            from aws_cdk.aws_lambda_event_sources import SnsEventSource
            
            # topic: sns.Topic
            
            # fn: lambda.Function
            
            dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
            fn.add_event_source(SnsEventSource(topic,
                filter_policy={},
                dead_letter_queue=dead_letter_queue
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52910378cab9bab930a889efbe6e8bc5ffa4d23e6a7ae409d7379da249b95120)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue]:
        '''Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_sns_889c7272.SubscriptionFilter]]:
        '''The filter policy.

        :default: - all messages are delivered
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_sns_889c7272.SubscriptionFilter]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq)
class SqsDlq(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.SqsDlq",
):
    '''An SQS dead letter queue destination configuration for a Lambda event source.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_dynamodb as dynamodb
        from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq
        
        # table: dynamodb.Table
        
        # fn: lambda.Function
        
        
        dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
        fn.add_event_source(DynamoEventSource(table,
            starting_position=lambda_.StartingPosition.TRIM_HORIZON,
            batch_size=5,
            bisect_batch_on_error=True,
            on_failure=SqsDlq(dead_letter_queue),
            retry_attempts=10
        ))
    '''

    def __init__(self, queue: _aws_cdk_aws_sqs_48bffef9.IQueue) -> None:
        '''
        :param queue: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3639095f19fb0555e541cfaac3683c98db4b970b900bab88dcdbd1db76a3e13d)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        jsii.create(self.__class__, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _target: _aws_cdk_aws_lambda_5443dbc3.IEventSourceMapping,
        target_handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    ) -> _aws_cdk_aws_lambda_5443dbc3.DlqDestinationConfig:
        '''Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0fbb5638b854bca147db547ab74a094126c02d5f914d281af315fd44d04798)
            check_type(argname="argument _target", value=_target, expected_type=type_hints["_target"])
            check_type(argname="argument target_handler", value=target_handler, expected_type=type_hints["target_handler"])
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.DlqDestinationConfig, jsii.invoke(self, "bind", [_target, target_handler]))


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSource)
class SqsEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.SqsEventSource",
):
    '''Use an Amazon SQS queue as an event source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_lambda_event_sources import SqsEventSource
        
        # fn: lambda.Function
        
        queue = sqs.Queue(self, "MyQueue")
        event_source = SqsEventSource(queue)
        fn.add_event_source(event_source)
        
        event_source_id = event_source.event_source_mapping_id
    '''

    def __init__(
        self,
        queue: _aws_cdk_aws_sqs_48bffef9.IQueue,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param queue: -
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. If ``maxBatchingWindow`` is configured, this value can go up to 10,000. Default: 10
        :param enabled: If the SQS event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Valid Range: Minimum value of 0 minutes. Maximum value of 5 minutes. Default: - no batching window. The lambda function will be invoked immediately with the records that are available.
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22245f40c5e1aae803a5dab0359b4f32f04cda271c54a76e93387a138323616e)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        props = SqsEventSourceProps(
            batch_size=batch_size,
            enabled=enabled,
            max_batching_window=max_batching_window,
            report_batch_item_failures=report_batch_item_failures,
        )

        jsii.create(self.__class__, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff10a796afc02061a8f638c629fa37e0503aaab882388d41e1c3dac7a629c4c)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''The identifier for this EventSourceMapping.'''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))

    @builtins.property
    @jsii.member(jsii_name="queue")
    def queue(self) -> _aws_cdk_aws_sqs_48bffef9.IQueue:
        return typing.cast(_aws_cdk_aws_sqs_48bffef9.IQueue, jsii.get(self, "queue"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.SqsEventSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "report_batch_item_failures": "reportBatchItemFailures",
    },
)
class SqsEventSourceProps:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. If ``maxBatchingWindow`` is configured, this value can go up to 10,000. Default: 10
        :param enabled: If the SQS event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Valid Range: Minimum value of 0 minutes. Maximum value of 5 minutes. Default: - no batching window. The lambda function will be invoked immediately with the records that are available.
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false

        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_lambda_event_sources import SqsEventSource
            # fn: lambda.Function
            
            
            queue = sqs.Queue(self, "MyQueue",
                visibility_timeout=Duration.seconds(30),  # default,
                receive_message_wait_time=Duration.seconds(20)
            )
            
            fn.add_event_source(SqsEventSource(queue,
                batch_size=10,  # default
                max_batching_window=Duration.minutes(5),
                report_batch_item_failures=True
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea3ac8e2c886f0f0c1c1b5181e9f22838f9423997f23e304d44369482387140)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument report_batch_item_failures", value=report_batch_item_failures, expected_type=type_hints["report_batch_item_failures"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if report_batch_item_failures is not None:
            self._values["report_batch_item_failures"] = report_batch_item_failures

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10.
        If ``maxBatchingWindow`` is configured, this value can go up to 10,000.

        :default: 10
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the SQS event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Valid Range: Minimum value of 0 minutes. Maximum value of 5 minutes.

        :default: - no batching window. The lambda function will be invoked immediately with the records that are available.
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def report_batch_item_failures(self) -> typing.Optional[builtins.bool]:
        '''Allow functions to return partially successful responses for a batch of records.

        :default: false

        :see: https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html#services-sqs-batchfailurereporting
        '''
        result = self._values.get("report_batch_item_failures")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IEventSource)
class StreamEventSource(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-lambda-event-sources.StreamEventSource",
):
    '''Use an stream as an event source for AWS Lambda.'''

    def __init__(
        self,
        *,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - the retention period configured on the stream
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: - discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: - retry until the record expires
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes. Default: - None
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        '''
        props = StreamEventSourceProps(
            bisect_batch_on_error=bisect_batch_on_error,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            report_batch_item_failures=report_batch_item_failures,
            retry_attempts=retry_attempts,
            tumbling_window=tumbling_window,
            starting_position=starting_position,
            batch_size=batch_size,
            enabled=enabled,
            max_batching_window=max_batching_window,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, _target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -
        '''
        ...

    @jsii.member(jsii_name="enrichMappingOptions")
    def _enrich_mapping_options(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        kafka_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        kafka_topic: typing.Optional[builtins.str] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        source_access_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_lambda_5443dbc3.SourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        starting_position: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.StartingPosition] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> _aws_cdk_aws_lambda_5443dbc3.EventSourceMappingOptions:
        '''
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis, Amazon DynamoDB, and Amazon MSK is 100 records. The default for Amazon SQS is 10 messages. For standard SQS queues, the maximum is 10,000. For FIFO SQS queues, the maximum is 10.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function. Default: - not set if using a self managed Kafka cluster, throws an error otherwise
        :param kafka_bootstrap_servers: A list of host and port pairs that are the addresses of the Kafka brokers in a self managed "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.example.com:9096``. Default: - none
        :param kafka_topic: The name of the Kafka topic. Default: - no topic
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - infinite or until the record expires.
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Set to ``undefined`` if you want lambda to keep retrying infinitely or until the record expires. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: - infinite or until the record expires.
        :param source_access_configurations: Specific settings like the authentication protocol or the VPC components to secure access to your event source. Default: - none
        :param starting_position: The position in the DynamoDB, Kinesis or MSK stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis, Amazon DynamoDB, and Amazon MSK Streams sources.
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis. Default: - None
        '''
        options = _aws_cdk_aws_lambda_5443dbc3.EventSourceMappingOptions(
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            event_source_arn=event_source_arn,
            kafka_bootstrap_servers=kafka_bootstrap_servers,
            kafka_topic=kafka_topic,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            report_batch_item_failures=report_batch_item_failures,
            retry_attempts=retry_attempts,
            source_access_configurations=source_access_configurations,
            starting_position=starting_position,
            tumbling_window=tumbling_window,
        )

        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.EventSourceMappingOptions, jsii.invoke(self, "enrichMappingOptions", [options]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "StreamEventSourceProps":
        return typing.cast("StreamEventSourceProps", jsii.get(self, "props"))


class _StreamEventSourceProxy(StreamEventSource):
    @jsii.member(jsii_name="bind")
    def bind(self, _target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008dda0cfe9aed3e8a89308614e49e283cab150e83a378e9e567d07c7e5648ff)
            check_type(argname="argument _target", value=_target, expected_type=type_hints["_target"])
        return typing.cast(None, jsii.invoke(self, "bind", [_target]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, StreamEventSource).__jsii_proxy_class__ = lambda : _StreamEventSourceProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.StreamEventSourceProps",
    jsii_struct_bases=[BaseStreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "bisect_batch_on_error": "bisectBatchOnError",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "report_batch_item_failures": "reportBatchItemFailures",
        "retry_attempts": "retryAttempts",
        "tumbling_window": "tumblingWindow",
    },
)
class StreamEventSourceProps(BaseStreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''The set of properties for streaming event sources shared by Dynamo and Kinesis.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - the retention period configured on the stream
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: - discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: - retry until the record expires
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes. Default: - None

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lambda as lambda_
            import aws_cdk.aws_lambda_event_sources as lambda_event_sources
            import aws_cdk.core as cdk
            
            # event_source_dlq: lambda.IEventSourceDlq
            
            stream_event_source_props = lambda_event_sources.StreamEventSourceProps(
                starting_position=lambda_.StartingPosition.TRIM_HORIZON,
            
                # the properties below are optional
                batch_size=123,
                bisect_batch_on_error=False,
                enabled=False,
                max_batching_window=cdk.Duration.minutes(30),
                max_record_age=cdk.Duration.minutes(30),
                on_failure=event_source_dlq,
                parallelization_factor=123,
                report_batch_item_failures=False,
                retry_attempts=123,
                tumbling_window=cdk.Duration.minutes(30)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aaedf8fe81710a067cc6e6a4cf0a354a207fc14918a4ad1f1d7b04d14bd6e89)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument bisect_batch_on_error", value=bisect_batch_on_error, expected_type=type_hints["bisect_batch_on_error"])
            check_type(argname="argument max_record_age", value=max_record_age, expected_type=type_hints["max_record_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument report_batch_item_failures", value=report_batch_item_failures, expected_type=type_hints["report_batch_item_failures"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument tumbling_window", value=tumbling_window, expected_type=type_hints["tumbling_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if report_batch_item_failures is not None:
            self._values["report_batch_item_failures"] = report_batch_item_failures
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if tumbling_window is not None:
            self._values["tumbling_window"] = tumbling_window

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''If the function returns an error, split the batch in two and retry.

        :default: false
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: - the retention period configured on the stream
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq]:
        '''An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: - discarded records are ignored
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def report_batch_item_failures(self) -> typing.Optional[builtins.bool]:
        '''Allow functions to return partially successful responses for a batch of records.

        :default: false

        :see: https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-ddb-batchfailurereporting
        '''
        result = self._values.get("report_batch_item_failures")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: - retry until the record expires
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tumbling_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes.

        :default: - None
        '''
        result = self._values.get("tumbling_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.DynamoEventSource",
):
    '''Use an Amazon DynamoDB stream as an event source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_dynamodb as dynamodb
        from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq
        
        # table: dynamodb.Table
        
        # fn: lambda.Function
        
        
        dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
        fn.add_event_source(DynamoEventSource(table,
            starting_position=lambda_.StartingPosition.TRIM_HORIZON,
            batch_size=5,
            bisect_batch_on_error=True,
            on_failure=SqsDlq(dead_letter_queue),
            retry_attempts=10
        ))
    '''

    def __init__(
        self,
        table: _aws_cdk_aws_dynamodb_eb1dc53b.ITable,
        *,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param table: -
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - the retention period configured on the stream
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: - discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: - retry until the record expires
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes. Default: - None
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02306e3abc81afdfcb83c089daf6adc26109ab66fb0fbfd2b27016c2ab9edaae)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        props = DynamoEventSourceProps(
            bisect_batch_on_error=bisect_batch_on_error,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            report_batch_item_failures=report_batch_item_failures,
            retry_attempts=retry_attempts,
            tumbling_window=tumbling_window,
            starting_position=starting_position,
            batch_size=batch_size,
            enabled=enabled,
            max_batching_window=max_batching_window,
        )

        jsii.create(self.__class__, self, [table, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e4b647937e80d5d215fe60649002d926344211300dbcbb26157dc1705f648a)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''The identifier for this EventSourceMapping.'''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.DynamoEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "bisect_batch_on_error": "bisectBatchOnError",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "report_batch_item_failures": "reportBatchItemFailures",
        "retry_attempts": "retryAttempts",
        "tumbling_window": "tumblingWindow",
    },
)
class DynamoEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - the retention period configured on the stream
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: - discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: - retry until the record expires
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes. Default: - None

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_dynamodb as dynamodb
            from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq
            
            # table: dynamodb.Table
            
            # fn: lambda.Function
            
            
            dead_letter_queue = sqs.Queue(self, "deadLetterQueue")
            fn.add_event_source(DynamoEventSource(table,
                starting_position=lambda_.StartingPosition.TRIM_HORIZON,
                batch_size=5,
                bisect_batch_on_error=True,
                on_failure=SqsDlq(dead_letter_queue),
                retry_attempts=10
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8a092e21caa00e185cd6c715596020545f0329cf1d5d71c7ecc9c423ef3571)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument bisect_batch_on_error", value=bisect_batch_on_error, expected_type=type_hints["bisect_batch_on_error"])
            check_type(argname="argument max_record_age", value=max_record_age, expected_type=type_hints["max_record_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument report_batch_item_failures", value=report_batch_item_failures, expected_type=type_hints["report_batch_item_failures"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument tumbling_window", value=tumbling_window, expected_type=type_hints["tumbling_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if report_batch_item_failures is not None:
            self._values["report_batch_item_failures"] = report_batch_item_failures
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if tumbling_window is not None:
            self._values["tumbling_window"] = tumbling_window

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''If the function returns an error, split the batch in two and retry.

        :default: false
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: - the retention period configured on the stream
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq]:
        '''An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: - discarded records are ignored
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def report_batch_item_failures(self) -> typing.Optional[builtins.bool]:
        '''Allow functions to return partially successful responses for a batch of records.

        :default: false

        :see: https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-ddb-batchfailurereporting
        '''
        result = self._values.get("report_batch_item_failures")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: - retry until the record expires
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tumbling_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes.

        :default: - None
        '''
        result = self._values.get("tumbling_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.KinesisEventSource",
):
    '''Use an Amazon Kinesis stream as an event source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesis as kinesis
        from aws_cdk.aws_lambda_event_sources import KinesisEventSource
        
        # my_function: lambda.Function
        
        
        stream = kinesis.Stream(self, "MyStream")
        my_function.add_event_source(KinesisEventSource(stream,
            batch_size=100,  # default
            starting_position=lambda_.StartingPosition.TRIM_HORIZON
        ))
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_0674c215.IStream,
        *,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param stream: -
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - the retention period configured on the stream
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: - discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: - retry until the record expires
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes. Default: - None
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62170ceb4b7cd68d0e4fd2740bffa58db490a3db8cdf0893c463e8211316053)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = KinesisEventSourceProps(
            bisect_batch_on_error=bisect_batch_on_error,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            report_batch_item_failures=report_batch_item_failures,
            retry_attempts=retry_attempts,
            tumbling_window=tumbling_window,
            starting_position=starting_position,
            batch_size=batch_size,
            enabled=enabled,
            max_batching_window=max_batching_window,
        )

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffbe0670e448247b3e06378fb8f5724f5fc99624ffc6b9d3a3f9273ea9a16d67)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''The identifier for this EventSourceMapping.'''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> _aws_cdk_aws_kinesis_0674c215.IStream:
        return typing.cast(_aws_cdk_aws_kinesis_0674c215.IStream, jsii.get(self, "stream"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-event-sources.KinesisEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "bisect_batch_on_error": "bisectBatchOnError",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "report_batch_item_failures": "reportBatchItemFailures",
        "retry_attempts": "retryAttempts",
        "tumbling_window": "tumblingWindow",
    },
)
class KinesisEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - the retention period configured on the stream
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: - discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: - retry until the record expires
        :param tumbling_window: The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes. Default: - None

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_kinesis as kinesis
            from aws_cdk.aws_lambda_event_sources import KinesisEventSource
            
            # my_function: lambda.Function
            
            
            stream = kinesis.Stream(self, "MyStream")
            my_function.add_event_source(KinesisEventSource(stream,
                batch_size=100,  # default
                starting_position=lambda_.StartingPosition.TRIM_HORIZON
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b8ba4d387e7739ba1e7a2a31abeba19b2e1fc0e3c49a13920f386bf50b4c36)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_batching_window", value=max_batching_window, expected_type=type_hints["max_batching_window"])
            check_type(argname="argument bisect_batch_on_error", value=bisect_batch_on_error, expected_type=type_hints["bisect_batch_on_error"])
            check_type(argname="argument max_record_age", value=max_record_age, expected_type=type_hints["max_record_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument report_batch_item_failures", value=report_batch_item_failures, expected_type=type_hints["report_batch_item_failures"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument tumbling_window", value=tumbling_window, expected_type=type_hints["tumbling_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if report_batch_item_failures is not None:
            self._values["report_batch_item_failures"] = report_batch_item_failures
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if tumbling_window is not None:
            self._values["tumbling_window"] = tumbling_window

    @builtins.property
    def starting_position(self) -> _aws_cdk_aws_lambda_5443dbc3.StartingPosition:
        '''Where to begin consuming the stream.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.StartingPosition, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource}

        :default: 100
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If the stream event source mapping should be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''If the function returns an error, split the batch in two and retry.

        :default: false
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: - the retention period configured on the stream
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq]:
        '''An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: - discarded records are ignored
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def report_batch_item_failures(self) -> typing.Optional[builtins.bool]:
        '''Allow functions to return partially successful responses for a batch of records.

        :default: false

        :see: https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-ddb-batchfailurereporting
        '''
        result = self._values.get("report_batch_item_failures")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: - retry until the record expires
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tumbling_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The size of the tumbling windows to group records sent to DynamoDB or Kinesis Valid Range: 0 - 15 minutes.

        :default: - None
        '''
        result = self._values.get("tumbling_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedKafkaEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.ManagedKafkaEventSource",
):
    '''Use a MSK cluster as a streaming source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_secretsmanager import Secret
        from aws_cdk.aws_lambda_event_sources import ManagedKafkaEventSource
        
        # my_function: lambda.Function
        
        
        # Your MSK cluster arn
        cluster_arn = "arn:aws:kafka:us-east-1:0123456789019:cluster/SalesCluster/abcd1234-abcd-cafe-abab-9876543210ab-4"
        
        # The Kafka topic you want to subscribe to
        topic = "some-cool-topic"
        
        # The secret that allows access to your MSK cluster
        # You still have to make sure that it is associated with your cluster as described in the documentation
        secret = Secret(self, "Secret", secret_name="AmazonMSK_KafkaSecret")
        my_function.add_event_source(ManagedKafkaEventSource(
            cluster_arn=cluster_arn,
            topic=topic,
            secret=secret,
            batch_size=100,  # default
            starting_position=lambda_.StartingPosition.TRIM_HORIZON
        ))
    '''

    def __init__(
        self,
        *,
        cluster_arn: builtins.str,
        topic: builtins.str,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param cluster_arn: An MSK cluster construct.
        :param topic: The Kafka topic to subscribe to.
        :param secret: The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet. Default: none
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        '''
        props = ManagedKafkaEventSourceProps(
            cluster_arn=cluster_arn,
            topic=topic,
            secret=secret,
            starting_position=starting_position,
            batch_size=batch_size,
            enabled=enabled,
            max_batching_window=max_batching_window,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef51689b0ac11135a64705453f0c6e243a2ac06597073e8eafe0d97ffc6e9ed2)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''The identifier for this EventSourceMapping.'''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))


class SelfManagedKafkaEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-event-sources.SelfManagedKafkaEventSource",
):
    '''Use a self hosted Kafka installation as a streaming source for AWS Lambda.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_secretsmanager import Secret
        from aws_cdk.aws_lambda_event_sources import SelfManagedKafkaEventSource
        
        # The secret that allows access to your self hosted Kafka cluster
        # secret: Secret
        
        # my_function: lambda.Function
        
        
        # The list of Kafka brokers
        bootstrap_servers = ["kafka-broker:9092"]
        
        # The Kafka topic you want to subscribe to
        topic = "some-cool-topic"
        my_function.add_event_source(SelfManagedKafkaEventSource(
            bootstrap_servers=bootstrap_servers,
            topic=topic,
            secret=secret,
            batch_size=100,  # default
            starting_position=lambda_.StartingPosition.TRIM_HORIZON
        ))
    '''

    def __init__(
        self,
        *,
        bootstrap_servers: typing.Sequence[builtins.str],
        authentication_method: typing.Optional[AuthenticationMethod] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        topic: builtins.str,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
        starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param bootstrap_servers: The list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.xyz.com:xxxx``.
        :param authentication_method: The authentication method for your Kafka cluster. Default: AuthenticationMethod.SASL_SCRAM_512_AUTH
        :param security_group: If your Kafka brokers are only reachable via VPC, provide the security group here. Default: - none, required if setting vpc
        :param vpc: If your Kafka brokers are only reachable via VPC provide the VPC here. Default: none
        :param vpc_subnets: If your Kafka brokers are only reachable via VPC, provide the subnets selection here. Default: - none, required if setting vpc
        :param topic: The Kafka topic to subscribe to.
        :param secret: The secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details This field is required if your Kafka brokers are accessed over the Internet. Default: none
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource}, {@link ManagedKafkaEventSource} and {@link SelfManagedKafkaEventSource} Default: 100
        :param enabled: If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        '''
        props = SelfManagedKafkaEventSourceProps(
            bootstrap_servers=bootstrap_servers,
            authentication_method=authentication_method,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            topic=topic,
            secret=secret,
            starting_position=starting_position,
            batch_size=batch_size,
            enabled=enabled,
            max_batching_window=max_batching_window,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f81f733e04f6d13d561b0153b924b6aa5cd774fc9280cbbe478446c9ad719e6)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "bind", [target]))


__all__ = [
    "ApiEventSource",
    "AuthenticationMethod",
    "BaseStreamEventSourceProps",
    "DynamoEventSource",
    "DynamoEventSourceProps",
    "KafkaEventSourceProps",
    "KinesisEventSource",
    "KinesisEventSourceProps",
    "ManagedKafkaEventSource",
    "ManagedKafkaEventSourceProps",
    "S3EventSource",
    "S3EventSourceProps",
    "SelfManagedKafkaEventSource",
    "SelfManagedKafkaEventSourceProps",
    "SnsDlq",
    "SnsEventSource",
    "SnsEventSourceProps",
    "SqsDlq",
    "SqsEventSource",
    "SqsEventSourceProps",
    "StreamEventSource",
    "StreamEventSourceProps",
]

publication.publish()

def _typecheckingstub__076fcd6efcc0dd0bc285557ce6dae238e8c87390924592dee0eab5aaad98924d(
    method: builtins.str,
    path: builtins.str,
    *,
    api_key_required: typing.Optional[builtins.bool] = None,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorization_type: typing.Optional[_aws_cdk_aws_apigateway_f01c2838.AuthorizationType] = None,
    authorizer: typing.Optional[_aws_cdk_aws_apigateway_f01c2838.IAuthorizer] = None,
    method_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_apigateway_f01c2838.MethodResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    operation_name: typing.Optional[builtins.str] = None,
    request_models: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_apigateway_f01c2838.IModel]] = None,
    request_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    request_validator: typing.Optional[_aws_cdk_aws_apigateway_f01c2838.IRequestValidator] = None,
    request_validator_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_f01c2838.RequestValidatorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffd76e94c35b3440c6f6fc5714a9d3141b8269baf677e4a5cc6d37864f51785(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6201a0056cd0f4ae8898f3c5ccda730f6c900993ff3bab23833f6e7c4d23b3(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e338a5a9e12b0674a4526b98f0e26b09ec5225de9b9e9ce6996864d9c86eef(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    topic: builtins.str,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a85299498386cebec70e76d822d45da40b4ce5130174d9873a4ee5b7d0db1f1(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    topic: builtins.str,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
    cluster_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9121bfbc3d21f50d01f9fb8c97b399a92c4e02e9e60d33ba4d314c7f3c13b9(
    bucket: _aws_cdk_aws_s3_55f001a5.Bucket,
    *,
    events: typing.Sequence[_aws_cdk_aws_s3_55f001a5.EventType],
    filters: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_55f001a5.NotificationKeyFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3eac6618bf058611b96de1366ce6807d697e843d3fff793fc5bae142eada82(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31c9a2adefdac1f8e285d3d2f83d6c23a006a88c833b5d1bc521f576579bd85(
    *,
    events: typing.Sequence[_aws_cdk_aws_s3_55f001a5.EventType],
    filters: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_55f001a5.NotificationKeyFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1da8aa7b61f62af23564d90cb79cb69ca13a3ec6d4c3bc3090291639a8cce3(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    topic: builtins.str,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_72af8d6f.ISecret] = None,
    bootstrap_servers: typing.Sequence[builtins.str],
    authentication_method: typing.Optional[AuthenticationMethod] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb126758e67d5dff286cacb1de18f6b4f622b879194a6ef539ef65992547a9b0(
    topic: _aws_cdk_aws_sns_889c7272.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a91847c9aa40be3b667209eb1fc27528e8bdf0e9a71701b0cd8bfdde1ce57d(
    _target: _aws_cdk_aws_lambda_5443dbc3.IEventSourceMapping,
    target_handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fe301a5781e6d4e8b042935df62070f7b9868b7fbb5c96150f76b4bf4f8397(
    topic: _aws_cdk_aws_sns_889c7272.ITopic,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_sns_889c7272.SubscriptionFilter]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3a63957448746235ed395874f9f97dacb0123e4be255920814c1434ace9b7b(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52910378cab9bab930a889efbe6e8bc5ffa4d23e6a7ae409d7379da249b95120(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_sns_889c7272.SubscriptionFilter]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3639095f19fb0555e541cfaac3683c98db4b970b900bab88dcdbd1db76a3e13d(
    queue: _aws_cdk_aws_sqs_48bffef9.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0fbb5638b854bca147db547ab74a094126c02d5f914d281af315fd44d04798(
    _target: _aws_cdk_aws_lambda_5443dbc3.IEventSourceMapping,
    target_handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22245f40c5e1aae803a5dab0359b4f32f04cda271c54a76e93387a138323616e(
    queue: _aws_cdk_aws_sqs_48bffef9.IQueue,
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff10a796afc02061a8f638c629fa37e0503aaab882388d41e1c3dac7a629c4c(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea3ac8e2c886f0f0c1c1b5181e9f22838f9423997f23e304d44369482387140(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008dda0cfe9aed3e8a89308614e49e283cab150e83a378e9e567d07c7e5648ff(
    _target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaedf8fe81710a067cc6e6a4cf0a354a207fc14918a4ad1f1d7b04d14bd6e89(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    bisect_batch_on_error: typing.Optional[builtins.bool] = None,
    max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02306e3abc81afdfcb83c089daf6adc26109ab66fb0fbfd2b27016c2ab9edaae(
    table: _aws_cdk_aws_dynamodb_eb1dc53b.ITable,
    *,
    bisect_batch_on_error: typing.Optional[builtins.bool] = None,
    max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e4b647937e80d5d215fe60649002d926344211300dbcbb26157dc1705f648a(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8a092e21caa00e185cd6c715596020545f0329cf1d5d71c7ecc9c423ef3571(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    bisect_batch_on_error: typing.Optional[builtins.bool] = None,
    max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62170ceb4b7cd68d0e4fd2740bffa58db490a3db8cdf0893c463e8211316053(
    stream: _aws_cdk_aws_kinesis_0674c215.IStream,
    *,
    bisect_batch_on_error: typing.Optional[builtins.bool] = None,
    max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbe0670e448247b3e06378fb8f5724f5fc99624ffc6b9d3a3f9273ea9a16d67(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b8ba4d387e7739ba1e7a2a31abeba19b2e1fc0e3c49a13920f386bf50b4c36(
    *,
    starting_position: _aws_cdk_aws_lambda_5443dbc3.StartingPosition,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    max_batching_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    bisect_batch_on_error: typing.Optional[builtins.bool] = None,
    max_record_age: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IEventSourceDlq] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    tumbling_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef51689b0ac11135a64705453f0c6e243a2ac06597073e8eafe0d97ffc6e9ed2(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f81f733e04f6d13d561b0153b924b6aa5cd774fc9280cbbe478446c9ad719e6(
    target: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass
