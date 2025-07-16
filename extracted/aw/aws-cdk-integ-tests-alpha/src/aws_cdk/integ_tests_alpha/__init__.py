r'''
# integ-tests

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Overview

This library is meant to be used in combination with the [integ-runner](https://github.com/aws/aws-cdk-cli/tree/main/packages/%40aws-cdk/integ-runner) CLI
to enable users to write and execute integration tests for AWS CDK Constructs.

An integration test should be defined as a CDK application, and
there should be a 1:1 relationship between an integration test and a CDK application.

So for example, in order to create an integration test called `my-function`
we would need to create a file to contain our integration test application.

*test/integ.my-function.ts*

```python
app = App()
stack = Stack()
lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
)
```

This is a self contained CDK application which we could deploy by running

```bash
cdk deploy --app 'node test/integ.my-function.js'
```

In order to turn this into an integration test, all that is needed is to
use the `IntegTest` construct.

```python
# app: App
# stack: Stack

IntegTest(app, "Integ", test_cases=[stack])
```

You will notice that the `stack` is registered to the `IntegTest` as a test case.
Each integration test can contain multiple test cases, which are just instances
of a stack. See the [Usage](#usage) section for more details.

## Usage

### IntegTest

Suppose you have a simple stack, that only encapsulates a Lambda function with a
certain handler:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )
```

You may want to test this stack under different conditions. For example, we want
this stack to be deployed correctly, regardless of the architecture we choose
for the Lambda function. In particular, it should work for both `ARM_64` and
`X86_64`. So you can create an `IntegTestCase` that exercises both scenarios:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )

# Beginning of the test suite
app = App()

IntegTest(app, "DifferentArchitectures",
    test_cases=[
        StackUnderTest(app, "Stack1",
            architecture=lambda_.Architecture.ARM_64
        ),
        StackUnderTest(app, "Stack2",
            architecture=lambda_.Architecture.X86_64
        )
    ]
)
```

This is all the instruction you need for the integration test runner to know
which stacks to synthesize, deploy and destroy. But you may also need to
customize the behavior of the runner by changing its parameters. For example:

```python
app = App()

stack_under_test = Stack(app, "StackUnderTest")

stack = Stack(app, "stack")

test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
    test_cases=[stack_under_test],
    diff_assets=True,
    stack_update_workflow=True,
    cdk_command_options=CdkCommands(
        deploy=DeployCommand(
            args=DeployOptions(
                require_approval=RequireApproval.NEVER,
                json=True
            )
        ),
        destroy=DestroyCommand(
            args=DestroyOptions(
                force=True
            )
        )
    )
)
```

### IntegTestCaseStack

In the majority of cases an integration test will contain a single `IntegTestCase`.
By default when you create an `IntegTest` an `IntegTestCase` is created for you
and all of your test cases are registered to this `IntegTestCase`. The `IntegTestCase`
and `IntegTestCaseStack` constructs are only needed when it is necessary to
defined different options for individual test cases.

For example, you might want to have one test case where `diffAssets` is enabled.

```python
# app: App
# stack_under_test: Stack

test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
    diff_assets=True
)

IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
```

## Assertions

This library also provides a utility to make assertions against the infrastructure that the integration test deploys.

There are two main scenarios in which assertions are created.

* Part of an integration test using `integ-runner`

In this case you would create an integration test using the `IntegTest` construct and then make assertions using the `assert` property.
You should **not** utilize the assertion constructs directly, but should instead use the `methods` on `IntegTest.assertions`.

```python
# app: App
# stack: Stack


integ = IntegTest(app, "Integ", test_cases=[stack])
integ.assertions.aws_api_call("S3", "getObject")
```

By default an assertions stack is automatically generated for you. You may however provide your own stack to use.

```python
# app: App
# stack: Stack
# assertion_stack: Stack


integ = IntegTest(app, "Integ", test_cases=[stack], assertion_stack=assertion_stack)
integ.assertions.aws_api_call("S3", "getObject")
```

* Part of a  normal CDK deployment

In this case you may be using assertions as part of a normal CDK deployment in order to make an assertion on the infrastructure
before the deployment is considered successful. In this case you can utilize the assertions constructs directly.

```python
# my_app_stack: Stack


AwsApiCall(my_app_stack, "GetObject",
    service="S3",
    api="getObject"
)
```

### DeployAssert

Assertions are created by using the `DeployAssert` construct. This construct creates it's own `Stack` separate from
any stacks that you create as part of your integration tests. This `Stack` is treated differently from other stacks
by the `integ-runner` tool. For example, this stack will not be diffed by the `integ-runner`.

`DeployAssert` also provides utilities to register your own assertions.

```python
# my_custom_resource: CustomResource
# stack: Stack
# app: App


integ = IntegTest(app, "Integ", test_cases=[stack])
integ.assertions.expect("CustomAssertion",
    ExpectedResult.object_like({"foo": "bar"}),
    ActualResult.from_custom_resource(my_custom_resource, "data"))
```

In the above example an assertion is created that will trigger a user defined `CustomResource`
and assert that the `data` attribute is equal to `{ foo: 'bar' }`.

### API Calls

A common method to retrieve the "actual" results to compare with what is expected is to make an
API call to receive some data. This library does this by utilizing CloudFormation custom resources
which means that CloudFormation will call out to a Lambda Function which will
make the API call.

#### HttpApiCall

Using the `HttpApiCall` will use the
[node-fetch](https://github.com/node-fetch/node-fetch) JavaScript library to
make the HTTP call.

This can be done by using the class directory (in the case of a normal deployment):

```python
# stack: Stack


HttpApiCall(stack, "MyAsssertion",
    url="https://example-api.com/abc"
)
```

Or by using the `httpApiCall` method on `DeployAssert` (when writing integration tests):

```python
# app: App
# stack: Stack

integ = IntegTest(app, "Integ",
    test_cases=[stack]
)
integ.assertions.http_api_call("https://example-api.com/abc")
```

#### AwsApiCall

Using the `AwsApiCall` construct will use the AWS JavaScript SDK to make the API call.

This can be done by using the class directory (in the case of a normal deployment):

```python
# stack: Stack


AwsApiCall(stack, "MyAssertion",
    service="SQS",
    api="receiveMessage",
    parameters={
        "QueueUrl": "url"
    }
)
```

Or by using the `awsApiCall` method on `DeployAssert` (when writing integration tests):

```python
# app: App
# stack: Stack

integ = IntegTest(app, "Integ",
    test_cases=[stack]
)
integ.assertions.aws_api_call("SQS", "receiveMessage", {
    "QueueUrl": "url"
})
```

You must specify the `service` and the `api` when using The `AwsApiCall` construct.
The `service` is the name of an AWS service, in one of the following forms:

* An AWS SDK for JavaScript v3 package name (`@aws-sdk/client-api-gateway`)
* An AWS SDK for JavaScript v3 client name (`api-gateway`)
* An AWS SDK for JavaScript v2 constructor name (`APIGateway`)
* A lowercase AWS SDK for JavaScript v2 constructor name (`apigateway`)

The `api` is the name of an AWS API call, in one of the following forms:

* An API call name as found in the API Reference documentation (`GetObject`)
* The API call name starting with a lowercase letter (`getObject`)
* The AWS SDK for JavaScript v3 command class name (`GetObjectCommand`)

By default, the `AwsApiCall` construct will automatically add the correct IAM policies
to allow the Lambda function to make the API call. It does this based on the `service`
and `api` that is provided. In the above example the service is `SQS` and the api is
`receiveMessage` so it will create a policy with `Action: 'sqs:ReceiveMessage`.

There are some cases where the permissions do not exactly match the service/api call, for
example the S3 `listObjectsV2` api. In these cases it is possible to add the correct policy
by accessing the `provider` object.

```python
# app: App
# stack: Stack
# integ: IntegTest


api_call = integ.assertions.aws_api_call("S3", "listObjectsV2", {
    "Bucket": "mybucket"
})

api_call.provider.add_to_role_policy({
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["*"]
})
```

When executing `waitForAssertion()`, it is necessary to add an IAM policy using `waiterProvider.addToRolePolicy()`.
Because `IApiCall` does not have a `waiterProvider` property, you need to cast it to `AwsApiCall`.

```python
# integ: IntegTest


api_call = integ.assertions.aws_api_call("S3", "listObjectsV2", {
    "Bucket": "mybucket"
}).wait_for_assertions()

api_call.waiter_provider.add_to_role_policy({
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["*"]
})
```

Note that addToRolePolicy() uses direct IAM JSON policy blobs, not a iam.PolicyStatement
object like you will see in the rest of the CDK.

### EqualsAssertion

This library currently provides the ability to assert that two values are equal
to one another by utilizing the `EqualsAssertion` class. This utilizes a Lambda
backed `CustomResource` which in tern uses the [Match](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html) utility from the
[@aws-cdk/assertions](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html) library.

```python
# app: App
# stack: Stack
# queue: sqs.Queue
# fn: lambda.IFunction


integ = IntegTest(app, "Integ",
    test_cases=[stack]
)

integ.assertions.invoke_function(
    function_name=fn.function_name,
    invocation_type=InvocationType.EVENT,
    payload=JSON.stringify({"status": "OK"})
)

message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
    "QueueUrl": queue.queue_url,
    "WaitTimeSeconds": 20
})

message.assert_at_path("Messages.0.Body", ExpectedResult.object_like({
    "request_context": {
        "condition": "Success"
    },
    "request_payload": {
        "status": "OK"
    },
    "response_context": {
        "status_code": 200
    },
    "response_payload": "success"
}))
```

#### Match

`integ-tests` also provides a `Match` utility similar to the `@aws-cdk/assertions` module. `Match`
can be used to construct the `ExpectedResult`. While the utility is similar, only a subset of methods are currently available on the `Match` utility of this module: `arrayWith`, `objectLike`, `stringLikeRegexp` and `serializedJson`.

```python
# message: AwsApiCall


message.expect(ExpectedResult.object_like({
    "Messages": Match.array_with([{
        "Payload": Match.serialized_json({"key": "value"})
    }, {
        "Body": {
            "Values": Match.array_with([{"Asdf": 3}]),
            "Message": Match.string_like_regexp("message")
        }
    }
    ])
}))
```

### Examples

#### Invoke a Lambda Function

In this example there is a Lambda Function that is invoked and
we assert that the payload that is returned is equal to '200'.

```python
# lambda_function: lambda.IFunction
# app: App


stack = Stack(app, "cdk-integ-lambda-bundling")

integ = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

invoke = integ.assertions.invoke_function(
    function_name=lambda_function.function_name
)
invoke.expect(ExpectedResult.object_like({
    "Payload": "200"
}))
```

The above example will by default create a CloudWatch log group that's never
expired. If you want to configure it with custom log retention days, you need
to specify the `logRetention` property.

```python
import aws_cdk.aws_logs as logs

# lambda_function: lambda.IFunction
# app: App


stack = Stack(app, "cdk-integ-lambda-bundling")

integ = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

invoke = integ.assertions.invoke_function(
    function_name=lambda_function.function_name,
    log_retention=logs.RetentionDays.ONE_WEEK
)
```

#### Make an AWS API Call

In this example there is a StepFunctions state machine that is executed
and then we assert that the result of the execution is successful.

```python
# app: App
# stack: Stack
# sm: IStateMachine


test_case = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

# Start an execution
start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
    "state_machine_arn": sm.state_machine_arn
})

# describe the results of the execution
describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
    "execution_arn": start.get_att_string("executionArn")
})

# assert the results
describe.expect(ExpectedResult.object_like({
    "status": "SUCCEEDED"
}))
```

#### Chain ApiCalls

Sometimes it may be necessary to chain API Calls. Since each API call is its own resource, all you
need to do is add a dependency between the calls. There is an helper method `next` that can be used.

```python
# integ: IntegTest


integ.assertions.aws_api_call("S3", "putObject", {
    "Bucket": "amzn-s3-demo-bucket",
    "Key": "my-key",
    "Body": "helloWorld"
}).next(integ.assertions.aws_api_call("S3", "getObject", {
    "Bucket": "amzn-s3-demo-bucket",
    "Key": "my-key"
}))
```

#### Wait for results

A common use case when performing assertions is to wait for a condition to pass. Sometimes the thing
that you are asserting against is not done provisioning by the time the assertion runs. In these
cases it is possible to run the assertion asynchronously by calling the `waitForAssertions()` method.

Taking the example above of executing a StepFunctions state machine, depending on the complexity of
the state machine, it might take a while for it to complete.

```python
# app: App
# stack: Stack
# sm: IStateMachine


test_case = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

# Start an execution
start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
    "state_machine_arn": sm.state_machine_arn
})

# describe the results of the execution
describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
    "execution_arn": start.get_att_string("executionArn")
}).expect(ExpectedResult.object_like({
    "status": "SUCCEEDED"
})).wait_for_assertions()
```

When you call `waitForAssertions()` the assertion provider will continuously make the `awsApiCall` until the
`ExpectedResult` is met. You can also control the parameters for waiting, for example:

```python
# test_case: IntegTest
# start: IApiCall


describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
    "execution_arn": start.get_att_string("executionArn")
}).expect(ExpectedResult.object_like({
    "status": "SUCCEEDED"
})).wait_for_assertions(
    total_timeout=Duration.minutes(5),
    interval=Duration.seconds(15),
    backoff_rate=3
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
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.cloud_assembly_schema as _aws_cdk_cloud_assembly_schema_ceddda9d
import constructs as _constructs_77d1e7e8


class ActualResult(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/integ-tests-alpha.ActualResult",
):
    '''(experimental) Represents the "actual" results to compare.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_custom_resource: CustomResource
        # stack: Stack
        # app: App
        
        
        integ = IntegTest(app, "Integ", test_cases=[stack])
        integ.assertions.expect("CustomAssertion",
            ExpectedResult.object_like({"foo": "bar"}),
            ActualResult.from_custom_resource(my_custom_resource, "data"))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAwsApiCall")
    @builtins.classmethod
    def from_aws_api_call(
        cls,
        query: "IApiCall",
        attribute: builtins.str,
    ) -> "ActualResult":
        '''(experimental) Get the actual results from a AwsApiCall.

        :param query: -
        :param attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8960192c69b2034028024915394db8e014653a8888980859f2e3547a455daa)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast("ActualResult", jsii.sinvoke(cls, "fromAwsApiCall", [query, attribute]))

    @jsii.member(jsii_name="fromCustomResource")
    @builtins.classmethod
    def from_custom_resource(
        cls,
        custom_resource: _aws_cdk_ceddda9d.CustomResource,
        attribute: builtins.str,
    ) -> "ActualResult":
        '''(experimental) Get the actual results from a CustomResource.

        :param custom_resource: -
        :param attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927c94a66cbe073d89039c4e27e1104a29d36865645ee1ba163e752be4da99a6)
            check_type(argname="argument custom_resource", value=custom_resource, expected_type=type_hints["custom_resource"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast("ActualResult", jsii.sinvoke(cls, "fromCustomResource", [custom_resource, attribute]))

    @builtins.property
    @jsii.member(jsii_name="result")
    @abc.abstractmethod
    def result(self) -> builtins.str:
        '''(experimental) The actual results as a string.

        :stability: experimental
        '''
        ...

    @result.setter
    @abc.abstractmethod
    def result(self, value: builtins.str) -> None:
        ...


class _ActualResultProxy(ActualResult):
    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        '''(experimental) The actual results as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @result.setter
    def result(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0def0e46807bcce5f5541c6cce0db0cd558065170e086f1248e1fbff32e95abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "result", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ActualResult).__jsii_proxy_class__ = lambda : _ActualResultProxy


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AssertionRequest",
    jsii_struct_bases=[],
    name_mapping={
        "actual": "actual",
        "expected": "expected",
        "fail_deployment": "failDeployment",
    },
)
class AssertionRequest:
    def __init__(
        self,
        *,
        actual: typing.Any,
        expected: typing.Any,
        fail_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) A request to make an assertion that the actual value matches the expected.

        :param actual: (experimental) The actual value received.
        :param expected: (experimental) The expected value to assert.
        :param fail_deployment: (experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure. This is only necessary if assertions are being executed outside of ``integ-runner``. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # actual: Any
            # expected: Any
            
            assertion_request = integ_tests_alpha.AssertionRequest(
                actual=actual,
                expected=expected,
            
                # the properties below are optional
                fail_deployment=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775e367a8b9b90eff85fd16c452c0ee84b1903d6aef4bbeec51fb738c386310b)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
            check_type(argname="argument fail_deployment", value=fail_deployment, expected_type=type_hints["fail_deployment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actual": actual,
            "expected": expected,
        }
        if fail_deployment is not None:
            self._values["fail_deployment"] = fail_deployment

    @builtins.property
    def actual(self) -> typing.Any:
        '''(experimental) The actual value received.

        :stability: experimental
        '''
        result = self._values.get("actual")
        assert result is not None, "Required property 'actual' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def expected(self) -> typing.Any:
        '''(experimental) The expected value to assert.

        :stability: experimental
        '''
        result = self._values.get("expected")
        assert result is not None, "Required property 'expected' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def fail_deployment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure.

        This is only necessary if assertions are being
        executed outside of ``integ-runner``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("fail_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AssertionResult",
    jsii_struct_bases=[],
    name_mapping={"assertion": "assertion", "failed": "failed"},
)
class AssertionResult:
    def __init__(
        self,
        *,
        assertion: builtins.str,
        failed: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The result of an Assertion wrapping the actual result data in another struct.

        Needed to access the whole message via getAtt() on the custom resource.

        :param assertion: (experimental) The result of an assertion.
        :param failed: (experimental) Whether or not the assertion failed. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            assertion_result = integ_tests_alpha.AssertionResult(
                assertion="assertion",
            
                # the properties below are optional
                failed=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75fa6e1a3201fe0fa6cf710bf3ea3f500448d16b191232e4e335385d56e566e)
            check_type(argname="argument assertion", value=assertion, expected_type=type_hints["assertion"])
            check_type(argname="argument failed", value=failed, expected_type=type_hints["failed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assertion": assertion,
        }
        if failed is not None:
            self._values["failed"] = failed

    @builtins.property
    def assertion(self) -> builtins.str:
        '''(experimental) The result of an assertion.

        :stability: experimental
        '''
        result = self._values.get("assertion")
        assert result is not None, "Required property 'assertion' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the assertion failed.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("failed")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AssertionResultData",
    jsii_struct_bases=[],
    name_mapping={"status": "status", "message": "message"},
)
class AssertionResultData:
    def __init__(
        self,
        *,
        status: "Status",
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The result of an assertion.

        :param status: (experimental) The status of the assertion, i.e. pass or fail.
        :param message: (experimental) Any message returned with the assertion result typically this will be the diff if there is any. Default: - none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            assertion_result_data = integ_tests_alpha.AssertionResultData(
                status=integ_tests_alpha.Status.PASS,
            
                # the properties below are optional
                message="message"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebef927d19dce3506807a648e225e27c5cee3900a2c2693bc29ecaad2d38101)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def status(self) -> "Status":
        '''(experimental) The status of the assertion, i.e. pass or fail.

        :stability: experimental
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast("Status", result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''(experimental) Any message returned with the assertion result typically this will be the diff if there is any.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionResultData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/integ-tests-alpha.AssertionType")
class AssertionType(enum.Enum):
    '''(experimental) The type of assertion to perform.

    :stability: experimental
    '''

    EQUALS = "EQUALS"
    '''(experimental) Assert that two values are equal.

    :stability: experimental
    '''
    OBJECT_LIKE = "OBJECT_LIKE"
    '''(experimental) The keys and their values must be present in the target but the target can be a superset.

    :stability: experimental
    '''
    ARRAY_WITH = "ARRAY_WITH"
    '''(experimental) Matches the specified pattern with the array The set of elements must be in the same order as would be found.

    :stability: experimental
    '''


class AssertionsProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.AssertionsProvider",
):
    '''(experimental) Represents an assertions provider.

    The creates a singletone
    Lambda Function that will create a single function per stack
    that serves as the custom resource provider for the various
    assertion providers

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.integ_tests_alpha as integ_tests_alpha
        from aws_cdk import aws_logs as logs
        
        assertions_provider = integ_tests_alpha.AssertionsProvider(self, "MyAssertionsProvider",
            handler="handler",
            log_retention=logs.RetentionDays.ONE_DAY,
            uuid="uuid"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        uuid: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param uuid: (experimental) This determines the uniqueness of each AssertionsProvider. You should only need to provide something different here if you *know* that you need a separate provider Default: - the default uuid is used
        :param handler: (experimental) The handler to use for the lambda function. Default: index.handler
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d829d3346bf088cede720be581add7c49c5142d6b67835d095d5b7fc2f3be071)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssertionsProviderProps(
            uuid=uuid, handler=handler, log_retention=log_retention
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addPolicyStatementFromSdkCall")
    def add_policy_statement_from_sdk_call(
        self,
        service: builtins.str,
        api: builtins.str,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Create a policy statement from a specific api call.

        :param service: -
        :param api: -
        :param resources: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285397c0e0cbfc08b4ceb96a2add1fa4e5526f2b30516e8392967f5137179e44)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        return typing.cast(None, jsii.invoke(self, "addPolicyStatementFromSdkCall", [service, api, resources]))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: typing.Any) -> None:
        '''(experimental) Add an IAM policy statement to the inline policy of the lambdas function's role.

        **Please note**: this is a direct IAM JSON policy blob, *not* a ``iam.PolicyStatement``
        object like you will see in the rest of the CDK.

        :param statement: -

        :stability: experimental

        Example::

            # provider: AssertionsProvider
            
            provider.add_to_role_policy({
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": ["*"]
            })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce43eeb4052a2bec14220d62d9e29dabfd6cd994cea93852c4eeea7119d694e)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="encode")
    def encode(self, obj: typing.Any) -> typing.Any:
        '''(experimental) Encode an object so it can be passed as custom resource parameters.

        Custom resources will convert
        all input parameters to strings so we encode non-strings here
        so we can then decode them correctly in the provider function

        :param obj: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aead2da0479681240000a232baddbe9a576e79f1bb8c553c4fc2eb15334792c)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(typing.Any, jsii.invoke(self, "encode", [obj]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, principal_arn: builtins.str) -> None:
        '''(experimental) Grant a principal access to invoke the assertion provider lambda function.

        :param principal_arn: the ARN of the principal that should be given permission to invoke the assertion provider.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15205a41c415f7c6befb41d2657e281256b15aca69cb25c1fe72c1803a5e34f8)
            check_type(argname="argument principal_arn", value=principal_arn, expected_type=type_hints["principal_arn"])
        return typing.cast(None, jsii.invoke(self, "grantInvoke", [principal_arn]))

    @builtins.property
    @jsii.member(jsii_name="handlerRoleArn")
    def handler_role_arn(self) -> _aws_cdk_ceddda9d.Reference:
        '''(experimental) A reference to the provider Lambda Function execution Role ARN.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.get(self, "handlerRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''(experimental) The ARN of the lambda function which can be used as a serviceToken to a CustomResource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AwsApiCallOptions",
    jsii_struct_bases=[],
    name_mapping={
        "api": "api",
        "service": "service",
        "output_paths": "outputPaths",
        "parameters": "parameters",
    },
)
class AwsApiCallOptions:
    def __init__(
        self,
        *,
        api: builtins.str,
        service: builtins.str,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) Options to perform an AWS JavaScript V2 API call.

        :param api: (experimental) The api call to make, i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service, i.e. S3.
        :param output_paths: (experimental) Restrict the data returned by the API call to specific paths in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Default: - return all data
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # parameters: Any
            
            aws_api_call_options = integ_tests_alpha.AwsApiCallOptions(
                api="api",
                service="service",
            
                # the properties below are optional
                output_paths=["outputPaths"],
                parameters=parameters
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb3bfb6e039f1770b7357b50e700e5397b1fe0af7e9bda38fcf799b232ae6b1)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument output_paths", value=output_paths, expected_type=type_hints["output_paths"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "service": service,
        }
        if output_paths is not None:
            self._values["output_paths"] = output_paths
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def api(self) -> builtins.str:
        '''(experimental) The api call to make, i.e. getBucketLifecycle.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The AWS service, i.e. S3.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Restrict the data returned by the API call to specific paths in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        :default: - return all data

        :stability: experimental
        '''
        result = self._values.get("output_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) Any parameters to pass to the api call.

        :default: - no parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AwsApiCallProps",
    jsii_struct_bases=[AwsApiCallOptions],
    name_mapping={
        "api": "api",
        "service": "service",
        "output_paths": "outputPaths",
        "parameters": "parameters",
    },
)
class AwsApiCallProps(AwsApiCallOptions):
    def __init__(
        self,
        *,
        api: builtins.str,
        service: builtins.str,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) Construct that creates a custom resource that will perform a query using the AWS SDK.

        :param api: (experimental) The api call to make, i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service, i.e. S3.
        :param output_paths: (experimental) Restrict the data returned by the API call to specific paths in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Default: - return all data
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_app_stack: Stack
            
            
            AwsApiCall(my_app_stack, "GetObject",
                service="S3",
                api="getObject"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9667093e2c183b6409c654dfeddf1ba9117d05548446571b59e368fb53b52357)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument output_paths", value=output_paths, expected_type=type_hints["output_paths"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "service": service,
        }
        if output_paths is not None:
            self._values["output_paths"] = output_paths
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def api(self) -> builtins.str:
        '''(experimental) The api call to make, i.e. getBucketLifecycle.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The AWS service, i.e. S3.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Restrict the data returned by the API call to specific paths in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        :default: - return all data

        :stability: experimental
        '''
        result = self._values.get("output_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) Any parameters to pass to the api call.

        :default: - no parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AwsApiCallRequest",
    jsii_struct_bases=[],
    name_mapping={
        "api": "api",
        "service": "service",
        "flatten_response": "flattenResponse",
        "output_paths": "outputPaths",
        "parameters": "parameters",
    },
)
class AwsApiCallRequest:
    def __init__(
        self,
        *,
        api: builtins.str,
        service: builtins.str,
        flatten_response: typing.Optional[builtins.str] = None,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) A AWS JavaScript SDK V2 request.

        :param api: (experimental) The AWS api call to make i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service i.e. S3.
        :param flatten_response: (experimental) Whether or not to flatten the response from the api call. Valid values are 'true' or 'false' as strings Typically when using an SdkRequest you will be passing it as the ``actual`` value to an assertion provider so this would be set to 'false' (you want the actual response). If you are using the SdkRequest to perform more of a query to return a single value to use, then this should be set to 'true'. For example, you could make a StepFunctions.startExecution api call and retrieve the ``executionArn`` from the response. Default: 'false'
        :param output_paths: (experimental) Restrict the data returned by the API call to specific paths in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Default: - return all data
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # parameters: Any
            
            aws_api_call_request = integ_tests_alpha.AwsApiCallRequest(
                api="api",
                service="service",
            
                # the properties below are optional
                flatten_response="flattenResponse",
                output_paths=["outputPaths"],
                parameters=parameters
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c5b4f02fb0af656efa41ad3e0b46bca31caf2520a4a6f541428609610641b2)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument flatten_response", value=flatten_response, expected_type=type_hints["flatten_response"])
            check_type(argname="argument output_paths", value=output_paths, expected_type=type_hints["output_paths"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "service": service,
        }
        if flatten_response is not None:
            self._values["flatten_response"] = flatten_response
        if output_paths is not None:
            self._values["output_paths"] = output_paths
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def api(self) -> builtins.str:
        '''(experimental) The AWS api call to make i.e. getBucketLifecycle.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The AWS service i.e. S3.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flatten_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether or not to flatten the response from the api call.

        Valid values are 'true' or 'false' as strings

        Typically when using an SdkRequest you will be passing it as the
        ``actual`` value to an assertion provider so this would be set
        to 'false' (you want the actual response).

        If you are using the SdkRequest to perform more of a query to return
        a single value to use, then this should be set to 'true'. For example,
        you could make a StepFunctions.startExecution api call and retrieve the
        ``executionArn`` from the response.

        :default: 'false'

        :stability: experimental
        '''
        result = self._values.get("flatten_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Restrict the data returned by the API call to specific paths in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        :default: - return all data

        :stability: experimental
        '''
        result = self._values.get("output_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) Any parameters to pass to the api call.

        :default: - no parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AwsApiCallResult",
    jsii_struct_bases=[],
    name_mapping={"api_call_response": "apiCallResponse"},
)
class AwsApiCallResult:
    def __init__(self, *, api_call_response: typing.Any) -> None:
        '''(experimental) The result from a SdkQuery.

        :param api_call_response: (experimental) The full api response.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # api_call_response: Any
            
            aws_api_call_result = integ_tests_alpha.AwsApiCallResult(
                api_call_response=api_call_response
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e3f1f73e49e1577977c7911e8cc8c5ef685546bdc133fdea8e9544cb4fd96b)
            check_type(argname="argument api_call_response", value=api_call_response, expected_type=type_hints["api_call_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_call_response": api_call_response,
        }

    @builtins.property
    def api_call_response(self) -> typing.Any:
        '''(experimental) The full api response.

        :stability: experimental
        '''
        result = self._values.get("api_call_response")
        assert result is not None, "Required property 'api_call_response' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EqualsAssertion(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.EqualsAssertion",
):
    '''(experimental) Construct that creates a CustomResource to assert that two values are equal.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.integ_tests_alpha as integ_tests_alpha
        
        # actual_result: integ_tests_alpha.ActualResult
        # expected_result: integ_tests_alpha.ExpectedResult
        
        equals_assertion = integ_tests_alpha.EqualsAssertion(self, "MyEqualsAssertion",
            actual=actual_result,
            expected=expected_result,
        
            # the properties below are optional
            fail_deployment=False
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        actual: ActualResult,
        expected: "ExpectedResult",
        fail_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param actual: (experimental) The actual results to compare.
        :param expected: (experimental) The expected result to assert.
        :param fail_deployment: (experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure. This is only necessary if assertions are being executed outside of ``integ-runner``. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c04e443c11a2367321899a4898db5e5d6620d46b9e0d1b3fa31d7e9dd021554)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EqualsAssertionProps(
            actual=actual, expected=expected, fail_deployment=fail_deployment
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        '''(experimental) The result of the assertion.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "result"))


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.EqualsAssertionProps",
    jsii_struct_bases=[],
    name_mapping={
        "actual": "actual",
        "expected": "expected",
        "fail_deployment": "failDeployment",
    },
)
class EqualsAssertionProps:
    def __init__(
        self,
        *,
        actual: ActualResult,
        expected: "ExpectedResult",
        fail_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for an EqualsAssertion.

        :param actual: (experimental) The actual results to compare.
        :param expected: (experimental) The expected result to assert.
        :param fail_deployment: (experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure. This is only necessary if assertions are being executed outside of ``integ-runner``. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # actual_result: integ_tests_alpha.ActualResult
            # expected_result: integ_tests_alpha.ExpectedResult
            
            equals_assertion_props = integ_tests_alpha.EqualsAssertionProps(
                actual=actual_result,
                expected=expected_result,
            
                # the properties below are optional
                fail_deployment=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58af14cdbf1ae6af7373273fada4bab47f80572e2dc79fc8406588336d4cd06a)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
            check_type(argname="argument fail_deployment", value=fail_deployment, expected_type=type_hints["fail_deployment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actual": actual,
            "expected": expected,
        }
        if fail_deployment is not None:
            self._values["fail_deployment"] = fail_deployment

    @builtins.property
    def actual(self) -> ActualResult:
        '''(experimental) The actual results to compare.

        :stability: experimental
        '''
        result = self._values.get("actual")
        assert result is not None, "Required property 'actual' is missing"
        return typing.cast(ActualResult, result)

    @builtins.property
    def expected(self) -> "ExpectedResult":
        '''(experimental) The expected result to assert.

        :stability: experimental
        '''
        result = self._values.get("expected")
        assert result is not None, "Required property 'expected' is missing"
        return typing.cast("ExpectedResult", result)

    @builtins.property
    def fail_deployment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure.

        This is only necessary if assertions are being
        executed outside of ``integ-runner``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("fail_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EqualsAssertionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpectedResult(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/integ-tests-alpha.ExpectedResult",
):
    '''(experimental) Represents the "expected" results to compare.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # stack: Stack
        # sm: IStateMachine
        
        
        test_case = IntegTest(app, "IntegTest",
            test_cases=[stack]
        )
        
        # Start an execution
        start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
            "state_machine_arn": sm.state_machine_arn
        })
        
        # describe the results of the execution
        describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
            "execution_arn": start.get_att_string("executionArn")
        })
        
        # assert the results
        describe.expect(ExpectedResult.object_like({
            "status": "SUCCEEDED"
        }))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="arrayWith")
    @builtins.classmethod
    def array_with(cls, expected: typing.Sequence[typing.Any]) -> "ExpectedResult":
        '''(experimental) The actual results must be a list and must contain an item with the expected results.

        :param expected: -

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html#static-arraywbrwithpattern
        :stability: experimental

        Example::

            # actual results
            actual = [{
                "string_param": "hello"
            }, {
                "string_param": "world"
            }
            ]
            # pass
            ExpectedResult.array_with([{
                "string_param": "hello"
            }
            ])
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f650c234de69311d3be1555c76c31b0bcf660ee568cb8877337aaa3fcc56a59)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "arrayWith", [expected]))

    @jsii.member(jsii_name="exact")
    @builtins.classmethod
    def exact(cls, expected: typing.Any) -> "ExpectedResult":
        '''(experimental) The actual results must match exactly.

        Missing data
        will result in a failure

        :param expected: -

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html#static-exactpattern
        :stability: experimental

        Example::

            # actual results
            actual = {
                "string_param": "hello",
                "number_param": 3,
                "boolean_param": True
            }
            # pass
            ExpectedResult.exact({
                "string_param": "hello",
                "number_param": 3,
                "boolean_param": True
            })
            
            # fail
            ExpectedResult.exact({
                "string_param": "hello"
            })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba1bd6868bcbf917d8781a68e462486356d1b72f71281beafa06866afb05e73)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "exact", [expected]))

    @jsii.member(jsii_name="objectLike")
    @builtins.classmethod
    def object_like(
        cls,
        expected: typing.Mapping[builtins.str, typing.Any],
    ) -> "ExpectedResult":
        '''(experimental) The expected results must be a subset of the actual results.

        :param expected: -

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html#static-objectwbrlikepattern
        :stability: experimental

        Example::

            # actual results
            actual = {
                "string_param": "hello",
                "number_param": 3,
                "boolean_param": True,
                "object_param": {"prop1": "value", "prop2": "value"}
            }
            # pass
            ExpectedResult.object_like({
                "string_param": "hello",
                "object_param": {"prop1": "value"}
            })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41760596828a67f336d3d40b1a2fade70ac97e61371e5de90c1ba47717728f61)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "objectLike", [expected]))

    @jsii.member(jsii_name="stringLikeRegexp")
    @builtins.classmethod
    def string_like_regexp(cls, expected: builtins.str) -> "ExpectedResult":
        '''(experimental) Actual results is a string that matches the Expected result regex.

        :param expected: -

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html#static-stringwbrlikewbrregexppattern
        :stability: experimental

        Example::

            # actual results
            actual = "some string value"
            
            # pass
            ExpectedResult.string_like_regexp("value")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba074a7cbb4cb81e3710d0722f59a4ad232869166467c789883b0d1ea35bf92)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "stringLikeRegexp", [expected]))

    @builtins.property
    @jsii.member(jsii_name="result")
    @abc.abstractmethod
    def result(self) -> builtins.str:
        '''(experimental) The expected results encoded as a string.

        :stability: experimental
        '''
        ...

    @result.setter
    @abc.abstractmethod
    def result(self, value: builtins.str) -> None:
        ...


class _ExpectedResultProxy(ExpectedResult):
    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        '''(experimental) The expected results encoded as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @result.setter
    def result(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33010e7c2f43ad7b078d998ca478ef09e6cf76bc2eadeb12407d48e7f8d56d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "result", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ExpectedResult).__jsii_proxy_class__ = lambda : _ExpectedResultProxy


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.FetchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "headers": "headers",
        "method": "method",
        "port": "port",
    },
)
class FetchOptions:
    def __init__(
        self,
        *,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options to pass to the JavaScript fetch api.

        :param body: (experimental) Request body. Default: - no body
        :param headers: (experimental) Optional request headers. Default: no headers
        :param method: (experimental) HTTP method. Default: GET
        :param port: (experimental) Optional port. Default: default port for protocol

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            fetch_options = integ_tests_alpha.FetchOptions(
                body="body",
                headers={
                    "headers_key": "headers"
                },
                method="method",
                port=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e88c6f6439b0e809ba451cf7d5fdcb3370b99a16f4d97c6d1c6ff524a91f56)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if headers is not None:
            self._values["headers"] = headers
        if method is not None:
            self._values["method"] = method
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''(experimental) Request body.

        :default: - no body

        :stability: experimental
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional request headers.

        :default: no headers

        :stability: experimental
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''(experimental) HTTP method.

        :default: GET

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Optional port.

        :default: default port for protocol

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FetchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.HttpRequest",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "flatten_response": "flattenResponse"},
)
class HttpRequest:
    def __init__(
        self,
        *,
        parameters: typing.Union["HttpRequestParameters", typing.Dict[builtins.str, typing.Any]],
        flatten_response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Request to the HttpCall resource.

        :param parameters: (experimental) Parameters from the custom resource.
        :param flatten_response: (experimental) Whether or not to flatten the response from the HTTP request. Valid values are 'true' or 'false' as strings Typically when using an HttpRequest you will be passing it as the ``actual`` value to an assertion provider so this would be set to 'false' (you want the actual response). If you are using the HttpRequest to perform more of a query to return a single value to use, then this should be set to 'true'. Default: 'false'

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            http_request = integ_tests_alpha.HttpRequest(
                parameters=integ_tests_alpha.HttpRequestParameters(
                    url="url",
            
                    # the properties below are optional
                    fetch_options=integ_tests_alpha.FetchOptions(
                        body="body",
                        headers={
                            "headers_key": "headers"
                        },
                        method="method",
                        port=123
                    )
                ),
            
                # the properties below are optional
                flatten_response="flattenResponse"
            )
        '''
        if isinstance(parameters, dict):
            parameters = HttpRequestParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e43070ab7c42531f81da281a2f078d3aaa5c2747ce7ed529dd5083e0ecf1f15)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument flatten_response", value=flatten_response, expected_type=type_hints["flatten_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameters": parameters,
        }
        if flatten_response is not None:
            self._values["flatten_response"] = flatten_response

    @builtins.property
    def parameters(self) -> "HttpRequestParameters":
        '''(experimental) Parameters from the custom resource.

        :stability: experimental
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast("HttpRequestParameters", result)

    @builtins.property
    def flatten_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether or not to flatten the response from the HTTP request.

        Valid values are 'true' or 'false' as strings

        Typically when using an HttpRequest you will be passing it as the
        ``actual`` value to an assertion provider so this would be set
        to 'false' (you want the actual response).

        If you are using the HttpRequest to perform more of a query to return
        a single value to use, then this should be set to 'true'.

        :default: 'false'

        :stability: experimental
        '''
        result = self._values.get("flatten_response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.HttpRequestParameters",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "fetch_options": "fetchOptions"},
)
class HttpRequestParameters:
    def __init__(
        self,
        *,
        url: builtins.str,
        fetch_options: typing.Optional[typing.Union[FetchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param url: (experimental) The url to fetch.
        :param fetch_options: (experimental) Options for fetch.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            http_request_parameters = integ_tests_alpha.HttpRequestParameters(
                url="url",
            
                # the properties below are optional
                fetch_options=integ_tests_alpha.FetchOptions(
                    body="body",
                    headers={
                        "headers_key": "headers"
                    },
                    method="method",
                    port=123
                )
            )
        '''
        if isinstance(fetch_options, dict):
            fetch_options = FetchOptions(**fetch_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93af9c54916c56a6f8f854ed0b3f9f13208556a5bdfc783196525c8d6ac46dab)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument fetch_options", value=fetch_options, expected_type=type_hints["fetch_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if fetch_options is not None:
            self._values["fetch_options"] = fetch_options

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The url to fetch.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fetch_options(self) -> typing.Optional[FetchOptions]:
        '''(experimental) Options for fetch.

        :stability: experimental
        '''
        result = self._values.get("fetch_options")
        return typing.cast(typing.Optional[FetchOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRequestParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.HttpResponse",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "headers": "headers",
        "ok": "ok",
        "status": "status",
        "status_text": "statusText",
    },
)
class HttpResponse:
    def __init__(
        self,
        *,
        body: typing.Any = None,
        headers: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        ok: typing.Optional[builtins.bool] = None,
        status: typing.Optional[jsii.Number] = None,
        status_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Response from fetch.

        :param body: (experimental) The response, either as parsed JSON or a string literal.
        :param headers: (experimental) Headers associated with the response.
        :param ok: (experimental) Indicates whether the response was successful. status range 200-299
        :param status: (experimental) Status code of the response.
        :param status_text: (experimental) The status message corresponding to the status code.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # body: Any
            # headers: Any
            
            http_response = integ_tests_alpha.HttpResponse(
                body=body,
                headers={
                    "headers_key": headers
                },
                ok=False,
                status=123,
                status_text="statusText"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391c496ab114dbafa2050e50cd71e9603e3723e49e2d262950bd96589530e06a)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument ok", value=ok, expected_type=type_hints["ok"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument status_text", value=status_text, expected_type=type_hints["status_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if headers is not None:
            self._values["headers"] = headers
        if ok is not None:
            self._values["ok"] = ok
        if status is not None:
            self._values["status"] = status
        if status_text is not None:
            self._values["status_text"] = status_text

    @builtins.property
    def body(self) -> typing.Any:
        '''(experimental) The response, either as parsed JSON or a string literal.

        :stability: experimental
        '''
        result = self._values.get("body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Headers associated with the response.

        :stability: experimental
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def ok(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the response was successful.

        status range 200-299

        :stability: experimental
        '''
        result = self._values.get("ok")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def status(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Status code of the response.

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status_text(self) -> typing.Optional[builtins.str]:
        '''(experimental) The status message corresponding to the status code.

        :stability: experimental
        '''
        result = self._values.get("status_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.HttpResponseWrapper",
    jsii_struct_bases=[],
    name_mapping={"api_call_response": "apiCallResponse"},
)
class HttpResponseWrapper:
    def __init__(
        self,
        *,
        api_call_response: typing.Union[HttpResponse, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Response from the HttpCall resource.

        :param api_call_response: (experimental) The Response from the fetch request.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            
            # body: Any
            # headers: Any
            
            http_response_wrapper = integ_tests_alpha.HttpResponseWrapper(
                api_call_response=integ_tests_alpha.HttpResponse(
                    body=body,
                    headers={
                        "headers_key": headers
                    },
                    ok=False,
                    status=123,
                    status_text="statusText"
                )
            )
        '''
        if isinstance(api_call_response, dict):
            api_call_response = HttpResponse(**api_call_response)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa97df0d1c119f8060810ef7873d7cbafff7b4b83e883dff6b5be3ec2fbbd17b)
            check_type(argname="argument api_call_response", value=api_call_response, expected_type=type_hints["api_call_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_call_response": api_call_response,
        }

    @builtins.property
    def api_call_response(self) -> HttpResponse:
        '''(experimental) The Response from the fetch request.

        :stability: experimental
        '''
        result = self._values.get("api_call_response")
        assert result is not None, "Required property 'api_call_response' is missing"
        return typing.cast(HttpResponse, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpResponseWrapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/integ-tests-alpha.IApiCall")
class IApiCall(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''(experimental) Represents an ApiCall.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> AssertionsProvider:
        '''(experimental) access the AssertionsProvider.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental

        Example::

            # api_call: AwsApiCall
            
            api_call.provider.add_to_role_policy({
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": ["*"]
            })
        '''
        ...

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(
        self,
        path: builtins.str,
        expected: ExpectedResult,
    ) -> "IApiCall":
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        Providing a path will filter the output of the initial API call.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            actual = {
                "Messages": [{
                    "MessageId": "",
                    "ReceiptHandle": "",
                    "MD5OfBody": "",
                    "Body": "hello",
                    "Attributes": {},
                    "MD5OfMessageAttributes": {},
                    "MessageAttributes": {}
                }]
            }
            message = integ.assertions.aws_api_call("SQS", "receiveMessage")
            
            message.assert_at_path("Messages.0.Body", ExpectedResult.string_like_regexp("hello"))
        '''
        ...

    @jsii.member(jsii_name="expect")
    def expect(self, expected: ExpectedResult) -> "IApiCall":
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall.

        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-func"
            )
            invoke.expect(ExpectedResult.object_like({"Payload": "OK"}))
        '''
        ...

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _aws_cdk_ceddda9d.Reference:
        '''(experimental) Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return:

        a token for ``Fn::GetAtt``. Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getAttString`` for string attributes.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''(experimental) Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return: a token for ``Fn::GetAtt`` encoded as a string.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="next")
    def next(self, next: "IApiCall") -> "IApiCall":
        '''(experimental) Allows you to chain IApiCalls. This adds an explicit dependency betweent the two resources.

        Returns the IApiCall provided as ``next``

        :param next: -

        :stability: experimental

        Example::

            # first: IApiCall
            # second: IApiCall
            
            
            first.next(second)
        '''
        ...

    @jsii.member(jsii_name="waitForAssertions")
    def wait_for_assertions(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> "IApiCall":
        '''(experimental) Wait for the IApiCall to return the expected response.

        If no expected response is specified then it will wait for
        the IApiCall to return a success

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental

        Example::

            # integ: IntegTest
            # execution_arn: str
            
            integ.assertions.aws_api_call("StepFunctions", "describeExecution", {
                "execution_arn": execution_arn
            }).wait_for_assertions()
        '''
        ...


class _IApiCallProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''(experimental) Represents an ApiCall.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/integ-tests-alpha.IApiCall"

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> AssertionsProvider:
        '''(experimental) access the AssertionsProvider.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental

        Example::

            # api_call: AwsApiCall
            
            api_call.provider.add_to_role_policy({
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": ["*"]
            })
        '''
        return typing.cast(AssertionsProvider, jsii.get(self, "provider"))

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        Providing a path will filter the output of the initial API call.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            actual = {
                "Messages": [{
                    "MessageId": "",
                    "ReceiptHandle": "",
                    "MD5OfBody": "",
                    "Body": "hello",
                    "Attributes": {},
                    "MD5OfMessageAttributes": {},
                    "MessageAttributes": {}
                }]
            }
            message = integ.assertions.aws_api_call("SQS", "receiveMessage")
            
            message.assert_at_path("Messages.0.Body", ExpectedResult.string_like_regexp("hello"))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f411c9c6ce09258efafb36af27db400c2f261d107ee630843a9353825628ab2a)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(IApiCall, jsii.invoke(self, "assertAtPath", [path, expected]))

    @jsii.member(jsii_name="expect")
    def expect(self, expected: ExpectedResult) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall.

        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-func"
            )
            invoke.expect(ExpectedResult.object_like({"Payload": "OK"}))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddf80736a88c6c822d6a25fbc32b7351e8da3accd460b8d16ff71eb55de6046)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(IApiCall, jsii.invoke(self, "expect", [expected]))

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _aws_cdk_ceddda9d.Reference:
        '''(experimental) Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return:

        a token for ``Fn::GetAtt``. Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getAttString`` for string attributes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfacb64b65fabe2392dc2b549890ca1c6de3d73472d8f4bbf082087228f4a805)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.invoke(self, "getAtt", [attribute_name]))

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''(experimental) Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return: a token for ``Fn::GetAtt`` encoded as a string.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecdf8894538ec23be7a00dac9133f608b80e8936665f4e1662ec5277f92ee17)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAttString", [attribute_name]))

    @jsii.member(jsii_name="next")
    def next(self, next: IApiCall) -> IApiCall:
        '''(experimental) Allows you to chain IApiCalls. This adds an explicit dependency betweent the two resources.

        Returns the IApiCall provided as ``next``

        :param next: -

        :stability: experimental

        Example::

            # first: IApiCall
            # second: IApiCall
            
            
            first.next(second)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bcab731afdde04f06b7b02cad97732570960e944e237d4caa43e6fbceaf938)
            check_type(argname="argument next", value=next, expected_type=type_hints["next"])
        return typing.cast(IApiCall, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="waitForAssertions")
    def wait_for_assertions(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> IApiCall:
        '''(experimental) Wait for the IApiCall to return the expected response.

        If no expected response is specified then it will wait for
        the IApiCall to return a success

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental

        Example::

            # integ: IntegTest
            # execution_arn: str
            
            integ.assertions.aws_api_call("StepFunctions", "describeExecution", {
                "execution_arn": execution_arn
            }).wait_for_assertions()
        '''
        options = WaiterStateMachineOptions(
            backoff_rate=backoff_rate, interval=interval, total_timeout=total_timeout
        )

        return typing.cast(IApiCall, jsii.invoke(self, "waitForAssertions", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApiCall).__jsii_proxy_class__ = lambda : _IApiCallProxy


@jsii.interface(jsii_type="@aws-cdk/integ-tests-alpha.IDeployAssert")
class IDeployAssert(typing_extensions.Protocol):
    '''(experimental) Interface that allows for registering a list of assertions that should be performed on a construct.

    This is only necessary
    when writing integration tests.

    :stability: experimental
    '''

    @jsii.member(jsii_name="awsApiCall")
    def aws_api_call(
        self,
        service: builtins.str,
        api: builtins.str,
        parameters: typing.Any = None,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> IApiCall:
        '''(experimental) Query AWS using JavaScript SDK API calls.

        This can be used to either
        trigger an action or to return a result that can then be asserted against
        an expected value

        The ``service`` is the name of an AWS service, in one of the following forms:

        - An AWS SDK for JavaScript v3 package name (``@aws-sdk/client-api-gateway``)
        - An AWS SDK for JavaScript v3 client name (``api-gateway``)
        - An AWS SDK for JavaScript v2 constructor name (``APIGateway``)
        - A lowercase AWS SDK for JavaScript v2 constructor name (``apigateway``)

        The ``api`` is the name of an AWS API call, in one of the following forms:

        - An API call name as found in the API Reference documentation (``GetObject``)
        - The API call name starting with a lowercase letter (``getObject``)
        - The AWS SDK for JavaScript v3 command class name (``GetObjectCommand``)

        :param service: -
        :param api: -
        :param parameters: -
        :param output_paths: -

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            integ.assertions.aws_api_call("SQS", "sendMessage", {
                "QueueUrl": "url",
                "MessageBody": "hello"
            })
            message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
                "QueueUrl": "url"
            })
            message.expect(ExpectedResult.object_like({
                "Messages": [{"Body": "hello"}]
            }))
        '''
        ...

    @jsii.member(jsii_name="expect")
    def expect(
        self,
        id: builtins.str,
        expected: ExpectedResult,
        actual: ActualResult,
    ) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the ActualResult.

        :param id: -
        :param expected: -
        :param actual: -

        :stability: experimental

        Example::

            # integ: IntegTest
            # api_call: AwsApiCall
            
            integ.assertions.expect("invoke",
                ExpectedResult.object_like({"Payload": "OK"}),
                ActualResult.from_aws_api_call(api_call, "Body"))
        '''
        ...

    @jsii.member(jsii_name="httpApiCall")
    def http_api_call(
        self,
        url: builtins.str,
        *,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> IApiCall:
        '''(experimental) Make an HTTP call to the provided endpoint.

        :param url: -
        :param body: (experimental) Request body. Default: - no body
        :param headers: (experimental) Optional request headers. Default: no headers
        :param method: (experimental) HTTP method. Default: GET
        :param port: (experimental) Optional port. Default: default port for protocol

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            call = integ.assertions.http_api_call("https://example.com/test")
            call.expect(ExpectedResult.object_like({
                "Message": "Hello World!"
            }))
        '''
        ...

    @jsii.member(jsii_name="invokeFunction")
    def invoke_function(
        self,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional["InvocationType"] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_type: typing.Optional["LogType"] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> IApiCall:
        '''(experimental) Invoke a lambda function and return the response which can be asserted.

        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONSE
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-function"
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        ...


class _IDeployAssertProxy:
    '''(experimental) Interface that allows for registering a list of assertions that should be performed on a construct.

    This is only necessary
    when writing integration tests.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/integ-tests-alpha.IDeployAssert"

    @jsii.member(jsii_name="awsApiCall")
    def aws_api_call(
        self,
        service: builtins.str,
        api: builtins.str,
        parameters: typing.Any = None,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> IApiCall:
        '''(experimental) Query AWS using JavaScript SDK API calls.

        This can be used to either
        trigger an action or to return a result that can then be asserted against
        an expected value

        The ``service`` is the name of an AWS service, in one of the following forms:

        - An AWS SDK for JavaScript v3 package name (``@aws-sdk/client-api-gateway``)
        - An AWS SDK for JavaScript v3 client name (``api-gateway``)
        - An AWS SDK for JavaScript v2 constructor name (``APIGateway``)
        - A lowercase AWS SDK for JavaScript v2 constructor name (``apigateway``)

        The ``api`` is the name of an AWS API call, in one of the following forms:

        - An API call name as found in the API Reference documentation (``GetObject``)
        - The API call name starting with a lowercase letter (``getObject``)
        - The AWS SDK for JavaScript v3 command class name (``GetObjectCommand``)

        :param service: -
        :param api: -
        :param parameters: -
        :param output_paths: -

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            integ.assertions.aws_api_call("SQS", "sendMessage", {
                "QueueUrl": "url",
                "MessageBody": "hello"
            })
            message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
                "QueueUrl": "url"
            })
            message.expect(ExpectedResult.object_like({
                "Messages": [{"Body": "hello"}]
            }))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0016b9ee68480906b65c3f2abda1a5eef570a527959ef608ac4d86836e7f4b28)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument output_paths", value=output_paths, expected_type=type_hints["output_paths"])
        return typing.cast(IApiCall, jsii.invoke(self, "awsApiCall", [service, api, parameters, output_paths]))

    @jsii.member(jsii_name="expect")
    def expect(
        self,
        id: builtins.str,
        expected: ExpectedResult,
        actual: ActualResult,
    ) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the ActualResult.

        :param id: -
        :param expected: -
        :param actual: -

        :stability: experimental

        Example::

            # integ: IntegTest
            # api_call: AwsApiCall
            
            integ.assertions.expect("invoke",
                ExpectedResult.object_like({"Payload": "OK"}),
                ActualResult.from_aws_api_call(api_call, "Body"))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5691b1933125f6e27b8109881a6206c07bcdea66d6a2a61d313cd6f7b30ce8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(None, jsii.invoke(self, "expect", [id, expected, actual]))

    @jsii.member(jsii_name="httpApiCall")
    def http_api_call(
        self,
        url: builtins.str,
        *,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> IApiCall:
        '''(experimental) Make an HTTP call to the provided endpoint.

        :param url: -
        :param body: (experimental) Request body. Default: - no body
        :param headers: (experimental) Optional request headers. Default: no headers
        :param method: (experimental) HTTP method. Default: GET
        :param port: (experimental) Optional port. Default: default port for protocol

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            call = integ.assertions.http_api_call("https://example.com/test")
            call.expect(ExpectedResult.object_like({
                "Message": "Hello World!"
            }))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9053497bae85d950ab08f20afee06c8e7c3e89c63f987e0320dba88e432ddff5)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        options = FetchOptions(body=body, headers=headers, method=method, port=port)

        return typing.cast(IApiCall, jsii.invoke(self, "httpApiCall", [url, options]))

    @jsii.member(jsii_name="invokeFunction")
    def invoke_function(
        self,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional["InvocationType"] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_type: typing.Optional["LogType"] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> IApiCall:
        '''(experimental) Invoke a lambda function and return the response which can be asserted.

        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONSE
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-function"
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        props = LambdaInvokeFunctionProps(
            function_name=function_name,
            invocation_type=invocation_type,
            log_retention=log_retention,
            log_type=log_type,
            payload=payload,
        )

        return typing.cast(IApiCall, jsii.invoke(self, "invokeFunction", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeployAssert).__jsii_proxy_class__ = lambda : _IDeployAssertProxy


class IntegTest(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.IntegTest",
):
    '''(experimental) A collection of test cases.

    Each test case file should contain exactly one
    instance of this class.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # stack: Stack
        # sm: IStateMachine
        
        
        test_case = IntegTest(app, "IntegTest",
            test_cases=[stack]
        )
        
        # Start an execution
        start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
            "state_machine_arn": sm.state_machine_arn
        })
        
        # describe the results of the execution
        describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
            "execution_arn": start.get_att_string("executionArn")
        })
        
        # assert the results
        describe.expect(ExpectedResult.object_like({
            "status": "SUCCEEDED"
        }))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        test_cases: typing.Sequence[_aws_cdk_ceddda9d.Stack],
        assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
        enable_lookups: typing.Optional[builtins.bool] = None,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param test_cases: (experimental) List of test cases that make up this test.
        :param assertion_stack: (experimental) Specify a stack to use for assertions. Default: - a stack is created for you
        :param enable_lookups: (experimental) Enable lookups for this test. If lookups are enabled then ``stackUpdateWorkflow`` must be set to false. Lookups should only be enabled when you are explicitly testing lookups. Default: false
        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fb8761c88b4fc9579f6a32db4edfe539963bdb489338e7e428d98f41281684)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IntegTestProps(
            test_cases=test_cases,
            assertion_stack=assertion_stack,
            enable_lookups=enable_lookups,
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> IDeployAssert:
        '''(experimental) Make assertions on resources in this test case.

        :stability: experimental
        '''
        return typing.cast(IDeployAssert, jsii.get(self, "assertions"))


class IntegTestCase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.IntegTestCase",
):
    '''(experimental) An integration test case. Allows the definition of test properties that apply to all stacks under this case.

    It is recommended that you use the IntegTest construct since that will create
    a default IntegTestCase

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.integ_tests_alpha as integ_tests_alpha
        import aws_cdk as cdk
        from aws_cdk import cloud_assembly_schema
        
        # stack: cdk.Stack
        
        integ_test_case = integ_tests_alpha.IntegTestCase(self, "MyIntegTestCase",
            stacks=[stack],
        
            # the properties below are optional
            allow_destroy=["allowDestroy"],
            assertion_stack=stack,
            cdk_command_options=CdkCommands(
                deploy=DeployCommand(
                    args=DeployOptions(
                        all=False,
                        app="app",
                        asset_metadata=False,
                        ca_bundle_path="caBundlePath",
                        change_set_name="changeSetName",
                        ci=False,
                        color=False,
                        concurrency=123,
                        context={
                            "context_key": "context"
                        },
                        debug=False,
                        ec2_creds=False,
                        exclusively=False,
                        execute=False,
                        force=False,
                        ignore_errors=False,
                        json=False,
                        lookups=False,
                        notices=False,
                        notification_arns=["notificationArns"],
                        output="output",
                        outputs_file="outputsFile",
                        parameters={
                            "parameters_key": "parameters"
                        },
                        path_metadata=False,
                        profile="profile",
                        proxy="proxy",
                        require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                        reuse_assets=["reuseAssets"],
                        role_arn="roleArn",
                        rollback=False,
                        stacks=["stacks"],
                        staging=False,
                        strict=False,
                        toolkit_stack_name="toolkitStackName",
                        trace=False,
                        use_previous_parameters=False,
                        verbose=False,
                        version_reporting=False
                    ),
                    enabled=False,
                    expected_message="expectedMessage",
                    expect_error=False
                ),
                destroy=DestroyCommand(
                    args=DestroyOptions(
                        all=False,
                        app="app",
                        asset_metadata=False,
                        ca_bundle_path="caBundlePath",
                        color=False,
                        context={
                            "context_key": "context"
                        },
                        debug=False,
                        ec2_creds=False,
                        exclusively=False,
                        force=False,
                        ignore_errors=False,
                        json=False,
                        lookups=False,
                        notices=False,
                        output="output",
                        path_metadata=False,
                        profile="profile",
                        proxy="proxy",
                        role_arn="roleArn",
                        stacks=["stacks"],
                        staging=False,
                        strict=False,
                        trace=False,
                        verbose=False,
                        version_reporting=False
                    ),
                    enabled=False,
                    expected_message="expectedMessage",
                    expect_error=False
                )
            ),
            diff_assets=False,
            hooks=Hooks(
                post_deploy=["postDeploy"],
                post_destroy=["postDestroy"],
                pre_deploy=["preDeploy"],
                pre_destroy=["preDestroy"]
            ),
            regions=["regions"],
            stack_update_workflow=False
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stacks: typing.Sequence[_aws_cdk_ceddda9d.Stack],
        assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stacks: (experimental) Stacks to be deployed during the test.
        :param assertion_stack: (experimental) Specify a stack to use for assertions. Default: - a stack is created for you
        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93909b22bdb434dd5bf6d9361625228bbeaf85254c3fc7bc9e72b77b70fd0e1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IntegTestCaseProps(
            stacks=stacks,
            assertion_stack=assertion_stack,
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> IDeployAssert:
        '''(experimental) Make assertions on resources in this test case.

        :stability: experimental
        '''
        return typing.cast(IDeployAssert, jsii.get(self, "assertions"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> _aws_cdk_cloud_assembly_schema_ceddda9d.IntegManifest:
        '''(experimental) The integration test manifest for this test case.

        Manifests are used
        by the integration test runner.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_cloud_assembly_schema_ceddda9d.IntegManifest, jsii.get(self, "manifest"))


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.IntegTestCaseProps",
    jsii_struct_bases=[_aws_cdk_cloud_assembly_schema_ceddda9d.TestOptions],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "stacks": "stacks",
        "assertion_stack": "assertionStack",
    },
)
class IntegTestCaseProps(_aws_cdk_cloud_assembly_schema_ceddda9d.TestOptions):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        stacks: typing.Sequence[_aws_cdk_ceddda9d.Stack],
        assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
    ) -> None:
        '''(experimental) Properties of an integration test case.

        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param stacks: (experimental) Stacks to be deployed during the test.
        :param assertion_stack: (experimental) Specify a stack to use for assertions. Default: - a stack is created for you

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            import aws_cdk as cdk
            from aws_cdk import cloud_assembly_schema
            
            # stack: cdk.Stack
            
            integ_test_case_props = integ_tests_alpha.IntegTestCaseProps(
                stacks=[stack],
            
                # the properties below are optional
                allow_destroy=["allowDestroy"],
                assertion_stack=stack,
                cdk_command_options=CdkCommands(
                    deploy=DeployCommand(
                        args=DeployOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            change_set_name="changeSetName",
                            ci=False,
                            color=False,
                            concurrency=123,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            execute=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            notification_arns=["notificationArns"],
                            output="output",
                            outputs_file="outputsFile",
                            parameters={
                                "parameters_key": "parameters"
                            },
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                            reuse_assets=["reuseAssets"],
                            role_arn="roleArn",
                            rollback=False,
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            toolkit_stack_name="toolkitStackName",
                            trace=False,
                            use_previous_parameters=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    ),
                    destroy=DestroyCommand(
                        args=DestroyOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            output="output",
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            role_arn="roleArn",
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            trace=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    )
                ),
                diff_assets=False,
                hooks=Hooks(
                    post_deploy=["postDeploy"],
                    post_destroy=["postDestroy"],
                    pre_deploy=["preDeploy"],
                    pre_destroy=["preDestroy"]
                ),
                regions=["regions"],
                stack_update_workflow=False
            )
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _aws_cdk_cloud_assembly_schema_ceddda9d.Hooks(**hooks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f36706ce503fa92c9baffb37b25208bc4e61071c2af78b1cf526c1916f483b6)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument assertion_stack", value=assertion_stack, expected_type=type_hints["assertion_stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow
        if assertion_stack is not None:
            self._values["assertion_stack"] = assertion_stack

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(
        self,
    ) -> typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands]:
        '''Additional options to use for each CDK command.

        :default: - runner default options
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks]:
        '''Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limit deployment to these regions.

        :default: - can run in any region
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stacks(self) -> typing.List[_aws_cdk_ceddda9d.Stack]:
        '''(experimental) Stacks to be deployed during the test.

        :stability: experimental
        '''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[_aws_cdk_ceddda9d.Stack], result)

    @builtins.property
    def assertion_stack(self) -> typing.Optional[_aws_cdk_ceddda9d.Stack]:
        '''(experimental) Specify a stack to use for assertions.

        :default: - a stack is created for you

        :stability: experimental
        '''
        result = self._values.get("assertion_stack")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Stack], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestCaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegTestCaseStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.IntegTestCaseStack",
):
    '''(experimental) An integration test case stack. Allows the definition of test properties that should apply to this stack.

    This should be used if there are multiple stacks in the integration test
    and it is necessary to specify different test case option for each. Otherwise
    normal stacks should be added to IntegTest

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # stack_under_test: Stack
        
        test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
            diff_assets=True
        )
        
        IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        property_injectors: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPropertyInjector]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param notification_arns: SNS Topic ARNs that will receive stack events. Default: - no notfication arns.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param property_injectors: A list of IPropertyInjector attached to this Stack. Default: - no PropertyInjectors
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Tags that will be applied to the Stack. These tags are applied to the CloudFormation Stack itself. They will not appear in the CloudFormation template. However, at deployment time, CloudFormation will apply these tags to all resources in the stack that support tagging. You will not be able to exempt resources from tagging (using the ``excludeResourceTypes`` property of ``Tags.of(...).add()``) for tags applied in this way. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3a10010962bdab5e34756e8b8781def4d66140bc39b762ac839b6431134b6e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IntegTestCaseStackProps(
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            notification_arns=notification_arns,
            permissions_boundary=permissions_boundary,
            property_injectors=property_injectors,
            stack_name=stack_name,
            suppress_template_indentation=suppress_template_indentation,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isIntegTestCaseStack")
    @builtins.classmethod
    def is_integ_test_case_stack(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Returns whether the construct is a IntegTestCaseStack.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0f2ea15e16068a7686e303272abe9b66aff6f74e31067127bd671e0b6dfd1a)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isIntegTestCaseStack", [x]))

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> IDeployAssert:
        '''(experimental) Make assertions on resources in this test case.

        :stability: experimental
        '''
        return typing.cast(IDeployAssert, jsii.get(self, "assertions"))


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.IntegTestCaseStackProps",
    jsii_struct_bases=[
        _aws_cdk_cloud_assembly_schema_ceddda9d.TestOptions,
        _aws_cdk_ceddda9d.StackProps,
    ],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "notification_arns": "notificationArns",
        "permissions_boundary": "permissionsBoundary",
        "property_injectors": "propertyInjectors",
        "stack_name": "stackName",
        "suppress_template_indentation": "suppressTemplateIndentation",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
    },
)
class IntegTestCaseStackProps(
    _aws_cdk_cloud_assembly_schema_ceddda9d.TestOptions,
    _aws_cdk_ceddda9d.StackProps,
):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        property_injectors: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPropertyInjector]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties of an integration test case stack.

        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param notification_arns: SNS Topic ARNs that will receive stack events. Default: - no notfication arns.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param property_injectors: A list of IPropertyInjector attached to this Stack. Default: - no PropertyInjectors
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Tags that will be applied to the Stack. These tags are applied to the CloudFormation Stack itself. They will not appear in the CloudFormation template. However, at deployment time, CloudFormation will apply these tags to all resources in the stack that support tagging. You will not be able to exempt resources from tagging (using the ``excludeResourceTypes`` property of ``Tags.of(...).add()``) for tags applied in this way. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # app: App
            # stack_under_test: Stack
            
            test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
                diff_assets=True
            )
            
            IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _aws_cdk_cloud_assembly_schema_ceddda9d.Hooks(**hooks)
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59edf2938a92df2253021d942b03a0fa818705ff3df6920854079be734c3e175)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument property_injectors", value=property_injectors, expected_type=type_hints["property_injectors"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument suppress_template_indentation", value=suppress_template_indentation, expected_type=type_hints["suppress_template_indentation"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if property_injectors is not None:
            self._values["property_injectors"] = property_injectors
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if suppress_template_indentation is not None:
            self._values["suppress_template_indentation"] = suppress_template_indentation
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(
        self,
    ) -> typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands]:
        '''Additional options to use for each CDK command.

        :default: - runner default options
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks]:
        '''Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limit deployment to these regions.

        :default: - can run in any region
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            # Use a concrete account and region to deploy this stack to:
            # `.account` and `.region` will simply return these values.
            Stack(app, "Stack1",
                env=Environment(
                    account="123456789012",
                    region="us-east-1"
                )
            )
            
            # Use the CLI's current credentials to determine the target environment:
            # `.account` and `.region` will reflect the account+region the CLI
            # is configured to use (based on the user CLI credentials)
            Stack(app, "Stack2",
                env=Environment(
                    account=process.env.CDK_DEFAULT_ACCOUNT,
                    region=process.env.CDK_DEFAULT_REGION
                )
            )
            
            # Define multiple stacks stage associated with an environment
            my_stage = Stage(app, "MyStage",
                env=Environment(
                    account="123456789012",
                    region="us-east-1"
                )
            )
            
            # both of these stacks will use the stage's account/region:
            # `.account` and `.region` will resolve to the concrete values as above
            MyStack(my_stage, "Stack1")
            YourStack(my_stage, "Stack2")
            
            # Define an environment-agnostic stack:
            # `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            # which will only resolve to actual values by CloudFormation during deployment.
            MyStack(app, "Stack1")
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''SNS Topic ARNs that will receive stack events.

        :default: - no notfication arns.
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary], result)

    @builtins.property
    def property_injectors(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.IPropertyInjector]]:
        '''A list of IPropertyInjector attached to this Stack.

        :default: - no PropertyInjectors
        '''
        result = self._values.get("property_injectors")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.IPropertyInjector]], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress_template_indentation(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to suppress indentation in generated CloudFormation templates.

        If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation``
        context key will be used. If that is not specified, then the
        default value ``false`` will be used.

        :default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        '''
        result = self._values.get("suppress_template_indentation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        The Stack Synthesizer controls aspects of synthesis and deployment,
        like how assets are referenced and what IAM roles to use. For more
        information, see the README of the main CDK package.

        If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used.
        If that is not specified, ``DefaultStackSynthesizer`` is used if
        ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major
        version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no
        other synthesizer is specified.

        :default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags that will be applied to the Stack.

        These tags are applied to the CloudFormation Stack itself. They will not
        appear in the CloudFormation template.

        However, at deployment time, CloudFormation will apply these tags to all
        resources in the stack that support tagging. You will not be able to exempt
        resources from tagging (using the ``excludeResourceTypes`` property of
        ``Tags.of(...).add()``) for tags applied in this way.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestCaseStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.IntegTestProps",
    jsii_struct_bases=[_aws_cdk_cloud_assembly_schema_ceddda9d.TestOptions],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "test_cases": "testCases",
        "assertion_stack": "assertionStack",
        "enable_lookups": "enableLookups",
    },
)
class IntegTestProps(_aws_cdk_cloud_assembly_schema_ceddda9d.TestOptions):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        test_cases: typing.Sequence[_aws_cdk_ceddda9d.Stack],
        assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
        enable_lookups: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Integration test properties.

        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param test_cases: (experimental) List of test cases that make up this test.
        :param assertion_stack: (experimental) Specify a stack to use for assertions. Default: - a stack is created for you
        :param enable_lookups: (experimental) Enable lookups for this test. If lookups are enabled then ``stackUpdateWorkflow`` must be set to false. Lookups should only be enabled when you are explicitly testing lookups. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # app: App
            # stack: Stack
            # sm: IStateMachine
            
            
            test_case = IntegTest(app, "IntegTest",
                test_cases=[stack]
            )
            
            # Start an execution
            start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
                "state_machine_arn": sm.state_machine_arn
            })
            
            # describe the results of the execution
            describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
                "execution_arn": start.get_att_string("executionArn")
            })
            
            # assert the results
            describe.expect(ExpectedResult.object_like({
                "status": "SUCCEEDED"
            }))
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _aws_cdk_cloud_assembly_schema_ceddda9d.Hooks(**hooks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2013546a0269b479331ed4cdfd706a8b20bf18d5f45e074d56ae77eb9b6dd4)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument test_cases", value=test_cases, expected_type=type_hints["test_cases"])
            check_type(argname="argument assertion_stack", value=assertion_stack, expected_type=type_hints["assertion_stack"])
            check_type(argname="argument enable_lookups", value=enable_lookups, expected_type=type_hints["enable_lookups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "test_cases": test_cases,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow
        if assertion_stack is not None:
            self._values["assertion_stack"] = assertion_stack
        if enable_lookups is not None:
            self._values["enable_lookups"] = enable_lookups

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(
        self,
    ) -> typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands]:
        '''Additional options to use for each CDK command.

        :default: - runner default options
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks]:
        '''Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limit deployment to these regions.

        :default: - can run in any region
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def test_cases(self) -> typing.List[_aws_cdk_ceddda9d.Stack]:
        '''(experimental) List of test cases that make up this test.

        :stability: experimental
        '''
        result = self._values.get("test_cases")
        assert result is not None, "Required property 'test_cases' is missing"
        return typing.cast(typing.List[_aws_cdk_ceddda9d.Stack], result)

    @builtins.property
    def assertion_stack(self) -> typing.Optional[_aws_cdk_ceddda9d.Stack]:
        '''(experimental) Specify a stack to use for assertions.

        :default: - a stack is created for you

        :stability: experimental
        '''
        result = self._values.get("assertion_stack")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Stack], result)

    @builtins.property
    def enable_lookups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable lookups for this test.

        If lookups are enabled
        then ``stackUpdateWorkflow`` must be set to false.
        Lookups should only be enabled when you are explicitly testing
        lookups.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_lookups")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/integ-tests-alpha.InvocationType")
class InvocationType(enum.Enum):
    '''(experimental) The type of invocation.

    Default is REQUEST_RESPONSE

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # stack: Stack
        # queue: sqs.Queue
        # fn: lambda.IFunction
        
        
        integ = IntegTest(app, "Integ",
            test_cases=[stack]
        )
        
        integ.assertions.invoke_function(
            function_name=fn.function_name,
            invocation_type=InvocationType.EVENT,
            payload=JSON.stringify({"status": "OK"})
        )
        
        message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
            "QueueUrl": queue.queue_url,
            "WaitTimeSeconds": 20
        })
        
        message.assert_at_path("Messages.0.Body", ExpectedResult.object_like({
            "request_context": {
                "condition": "Success"
            },
            "request_payload": {
                "status": "OK"
            },
            "response_context": {
                "status_code": 200
            },
            "response_payload": "success"
        }))
    '''

    EVENT = "EVENT"
    '''(experimental) Invoke the function asynchronously.

    Send events that fail multiple times to the function's
    dead-letter queue (if it's configured).
    The API response only includes a status code.

    :stability: experimental
    '''
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''(experimental) Invoke the function synchronously.

    Keep the connection open until the function returns a response or times out.
    The API response includes the function response and additional data.

    :stability: experimental
    '''
    DRY_RUN = "DRY_RUN"
    '''(experimental) Validate parameter values and verify that the user or role has permission to invoke the function.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.LambdaFunctionProviderProps",
    jsii_struct_bases=[],
    name_mapping={"handler": "handler", "log_retention": "logRetention"},
)
class LambdaFunctionProviderProps:
    def __init__(
        self,
        *,
        handler: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''(experimental) Properties for a lambda function provider.

        :param handler: (experimental) The handler to use for the lambda function. Default: index.handler
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            from aws_cdk import aws_logs as logs
            
            lambda_function_provider_props = integ_tests_alpha.LambdaFunctionProviderProps(
                handler="handler",
                log_retention=logs.RetentionDays.ONE_DAY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38d440a6e46009e1964a16dca6cca6a65cee4a96c1e4ec4505f3cc068bc45c1)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if handler is not None:
            self._values["handler"] = handler
        if log_retention is not None:
            self._values["log_retention"] = log_retention

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''(experimental) The handler to use for the lambda function.

        :default: index.handler

        :stability: experimental
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) How long, in days, the log contents will be retained.

        :default: - no retention days specified

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.LambdaInvokeFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "invocation_type": "invocationType",
        "log_retention": "logRetention",
        "log_type": "logType",
        "payload": "payload",
    },
)
class LambdaInvokeFunctionProps:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional[InvocationType] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_type: typing.Optional["LogType"] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to pass to the Lambda invokeFunction API call.

        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONSE
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # lambda_function: lambda.IFunction
            # app: App
            
            
            stack = Stack(app, "cdk-integ-lambda-bundling")
            
            integ = IntegTest(app, "IntegTest",
                test_cases=[stack]
            )
            
            invoke = integ.assertions.invoke_function(
                function_name=lambda_function.function_name
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f94aeefe8016f3f35355f86e35cc34b53e597152be16a8b6a678afab636d7b)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
        }
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_type is not None:
            self._values["log_type"] = log_type
        if payload is not None:
            self._values["payload"] = payload

    @builtins.property
    def function_name(self) -> builtins.str:
        '''(experimental) The name of the function to invoke.

        :stability: experimental
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[InvocationType]:
        '''(experimental) The type of invocation to use.

        :default: InvocationType.REQUEST_RESPONSE

        :stability: experimental
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[InvocationType], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) How long, in days, the log contents will be retained.

        :default: - no retention days specified

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def log_type(self) -> typing.Optional["LogType"]:
        '''(experimental) Whether to return the logs as part of the response.

        :default: LogType.NONE

        :stability: experimental
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional["LogType"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) Payload to send as part of the invoke.

        :default: - no payload

        :stability: experimental
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaInvokeFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/integ-tests-alpha.LogType")
class LogType(enum.Enum):
    '''(experimental) Set to Tail to include the execution log in the response.

    Applies to synchronously invoked functions only.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) The log messages are not returned in the response.

    :stability: experimental
    '''
    TAIL = "TAIL"
    '''(experimental) The log messages are returned in the response.

    :stability: experimental
    '''


class Match(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/integ-tests-alpha.Match",
):
    '''(experimental) Partial and special matching during assertions.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="arrayWith")
    @builtins.classmethod
    def array_with(
        cls,
        pattern: typing.Sequence[typing.Any],
    ) -> typing.Mapping[builtins.str, typing.List[typing.Any]]:
        '''(experimental) Matches the specified pattern with the array found in the same relative path of the target.

        The set of elements (or matchers) must be in the same order as would be found.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cd8dd33ba371f84a9b655b09b12aca9fda33749b1d492e04e29de74e17ce19)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, typing.List[typing.Any]], jsii.sinvoke(cls, "arrayWith", [pattern]))

    @jsii.member(jsii_name="objectLike")
    @builtins.classmethod
    def object_like(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Matches the specified pattern to an object found in the same relative path of the target.

        The keys and their values (or matchers) must be present in the target but the target can be a superset.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ed9ce4ac8ba15c74fcb4d77253ca710ec1f313d1f47ebb3641222f363fc260)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.sinvoke(cls, "objectLike", [pattern]))

    @jsii.member(jsii_name="serializedJson")
    @builtins.classmethod
    def serialized_json(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Matches any string-encoded JSON and applies the specified pattern after parsing it.

        :param pattern: the pattern to match after parsing the encoded JSON.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6f20a7536a39c152b01944858b6ec7920308d8ab4b26ce4ca075855f0c4aae)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.sinvoke(cls, "serializedJson", [pattern]))

    @jsii.member(jsii_name="stringLikeRegexp")
    @builtins.classmethod
    def string_like_regexp(
        cls,
        pattern: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Matches targets according to a regular expression.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b86e0fb528b0809c81fd8c9509acd452ec22cd078f57824f27506c9ac85d9b)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sinvoke(cls, "stringLikeRegexp", [pattern]))


class _MatchProxy(Match):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Match).__jsii_proxy_class__ = lambda : _MatchProxy


@jsii.enum(jsii_type="@aws-cdk/integ-tests-alpha.Status")
class Status(enum.Enum):
    '''(experimental) The status of the assertion.

    :stability: experimental
    '''

    PASS = "PASS"
    '''(experimental) The assertion passed.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) The assertion failed.

    :stability: experimental
    '''


class WaiterStateMachine(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.WaiterStateMachine",
):
    '''(experimental) A very simple StateMachine construct highly customized to the provider framework.

    This is so that this package does not need to depend on aws-stepfunctions module.

    The state machine continuously calls the isCompleteHandler, until it succeeds or times out.
    The handler is called ``maxAttempts`` times with an ``interval`` duration and a ``backoffRate`` rate.

    For example with:

    - maxAttempts = 360 (30 minutes)
    - interval = 5
    - backoffRate = 1 (no backoff)

    it will make the API Call every 5 seconds and fail after 360 failures.

    If the backoff rate is changed to 2 (for example), it will

    - make the first call
    - wait 5 seconds
    - make the second call
    - wait 15 seconds
    - etc.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.integ_tests_alpha as integ_tests_alpha
        import aws_cdk as cdk
        
        waiter_state_machine = integ_tests_alpha.WaiterStateMachine(self, "MyWaiterStateMachine",
            backoff_rate=123,
            interval=cdk.Duration.minutes(30),
            total_timeout=cdk.Duration.minutes(30)
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99521e6ae1132d620337d92d0e6db2d69a603a34b4b8ff711ffc16a33f710a3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WaiterStateMachineProps(
            backoff_rate=backoff_rate, interval=interval, total_timeout=total_timeout
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="isCompleteProvider")
    def is_complete_provider(self) -> AssertionsProvider:
        '''(experimental) The AssertionsProvide that handles async requests.

        :stability: experimental
        '''
        return typing.cast(AssertionsProvider, jsii.get(self, "isCompleteProvider"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''(experimental) The IAM Role ARN of the role used by the state machine.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> builtins.str:
        '''(experimental) The ARN of the statemachine.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateMachineArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.WaiterStateMachineOptions",
    jsii_struct_bases=[],
    name_mapping={
        "backoff_rate": "backoffRate",
        "interval": "interval",
        "total_timeout": "totalTimeout",
    },
)
class WaiterStateMachineOptions:
    def __init__(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''(experimental) Options for creating a WaiterStateMachine.

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        :exampleMetadata: lit=../@aws-cdk-testing/framework-integ/test/aws-kinesisfirehose/test/integ.s3-bucket.lit.ts infused

        Example::

            import path as path
            import aws_cdk.aws_kinesisfirehose as firehose
            import aws_cdk.aws_kms as kms
            import aws_cdk.aws_lambda_nodejs as lambdanodejs
            import aws_cdk.aws_logs as logs
            import aws_cdk.aws_s3 as s3
            import aws_cdk as cdk
            from aws_cdk.integ_tests_alpha import AwsApiCall, ExpectedResult, IntegTest
            
            app = cdk.App(
                post_cli_context={
                    "@aws-cdk/aws-lambda:useCdkManagedLogGroup": False
                }
            )
            
            stack = cdk.Stack(app, "aws-cdk-firehose-delivery-stream-s3-all-properties")
            
            bucket = s3.Bucket(stack, "FirehoseDeliveryStreamS3AllPropertiesBucket",
                removal_policy=cdk.RemovalPolicy.DESTROY,
                auto_delete_objects=True
            )
            
            backup_bucket = s3.Bucket(stack, "FirehoseDeliveryStreamS3AllPropertiesBackupBucket",
                removal_policy=cdk.RemovalPolicy.DESTROY,
                auto_delete_objects=True
            )
            log_group = logs.LogGroup(stack, "LogGroup",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
            
            data_processor_function = lambdanodejs.NodejsFunction(stack, "DataProcessorFunction",
                entry=path.join(__dirname, "lambda-data-processor.js"),
                timeout=cdk.Duration.minutes(1)
            )
            
            processor = firehose.LambdaFunctionProcessor(data_processor_function,
                buffer_interval=cdk.Duration.seconds(60),
                buffer_size=cdk.Size.mebibytes(1),
                retries=1
            )
            
            key = kms.Key(stack, "Key",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
            
            backup_key = kms.Key(stack, "BackupKey",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
            
            delivery_stream = firehose.DeliveryStream(stack, "DeliveryStream",
                destination=firehose.S3Bucket(bucket,
                    logging_config=firehose.EnableLogging(log_group),
                    processor=processor,
                    compression=firehose.Compression.GZIP,
                    data_output_prefix="regularPrefix",
                    error_output_prefix="errorPrefix",
                    file_extension=".log.gz",
                    time_zone=cdk.TimeZone.ASIA_TOKYO,
                    buffering_interval=cdk.Duration.seconds(60),
                    buffering_size=cdk.Size.mebibytes(1),
                    encryption_key=key,
                    s3_backup=firehose.DestinationS3BackupProps(
                        mode=firehose.BackupMode.ALL,
                        bucket=backup_bucket,
                        compression=firehose.Compression.ZIP,
                        data_output_prefix="backupPrefix",
                        error_output_prefix="backupErrorPrefix",
                        buffering_interval=cdk.Duration.seconds(60),
                        buffering_size=cdk.Size.mebibytes(1),
                        encryption_key=backup_key
                    )
                )
            )
            
            firehose.DeliveryStream(stack, "ZeroBufferingDeliveryStream",
                destination=firehose.S3Bucket(bucket,
                    compression=firehose.Compression.GZIP,
                    data_output_prefix="regularPrefix",
                    error_output_prefix="errorPrefix",
                    buffering_interval=cdk.Duration.seconds(0)
                )
            )
            
            test_case = IntegTest(app, "integ-tests",
                test_cases=[stack],
                regions=["us-east-1"]
            )
            
            test_case.assertions.aws_api_call("Firehose", "putRecord", {
                "DeliveryStreamName": delivery_stream.delivery_stream_name,
                "Record": {
                    "Data": "testData123"
                }
            })
            
            s3_api_call = test_case.assertions.aws_api_call("S3", "listObjectsV2", {
                "Bucket": bucket.bucket_name,
                "MaxKeys": 1
            }).expect(ExpectedResult.object_like({
                "KeyCount": 1
            })).wait_for_assertions(
                interval=cdk.Duration.seconds(30),
                total_timeout=cdk.Duration.minutes(10)
            )
            
            if s3_api_call instanceof AwsApiCall && s3_api_call.waiter_provider:
                s3_api_call.waiter_provider.add_to_role_policy({
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:ListBucket"],
                    "Resource": ["*"]
                })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121fca5df71218eb18c08109872208325ee23307067d82bcba84288b6feccd22)
            check_type(argname="argument backoff_rate", value=backoff_rate, expected_type=type_hints["backoff_rate"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument total_timeout", value=total_timeout, expected_type=type_hints["total_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backoff_rate is not None:
            self._values["backoff_rate"] = backoff_rate
        if interval is not None:
            self._values["interval"] = interval
        if total_timeout is not None:
            self._values["total_timeout"] = total_timeout

    @builtins.property
    def backoff_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Backoff between attempts.

        This is the multiplier by which the retry interval increases
        after each retry attempt.

        By default there is no backoff. Each retry will wait the amount of time
        specified by ``interval``.

        :default: 1 (no backoff)

        :stability: experimental
        '''
        result = self._values.get("backoff_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The interval (number of seconds) to wait between attempts.

        :default: Duration.seconds(5)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def total_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The total time that the state machine will wait for a successful response.

        :default: Duration.minutes(30)

        :stability: experimental
        '''
        result = self._values.get("total_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaiterStateMachineOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.WaiterStateMachineProps",
    jsii_struct_bases=[WaiterStateMachineOptions],
    name_mapping={
        "backoff_rate": "backoffRate",
        "interval": "interval",
        "total_timeout": "totalTimeout",
    },
)
class WaiterStateMachineProps(WaiterStateMachineOptions):
    def __init__(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''(experimental) Props for creating a WaiterStateMachine.

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            import aws_cdk as cdk
            
            waiter_state_machine_props = integ_tests_alpha.WaiterStateMachineProps(
                backoff_rate=123,
                interval=cdk.Duration.minutes(30),
                total_timeout=cdk.Duration.minutes(30)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e828ea92e322e9108a7c287fff81908fdb3933543431b12a3a1c1252a39520e)
            check_type(argname="argument backoff_rate", value=backoff_rate, expected_type=type_hints["backoff_rate"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument total_timeout", value=total_timeout, expected_type=type_hints["total_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backoff_rate is not None:
            self._values["backoff_rate"] = backoff_rate
        if interval is not None:
            self._values["interval"] = interval
        if total_timeout is not None:
            self._values["total_timeout"] = total_timeout

    @builtins.property
    def backoff_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Backoff between attempts.

        This is the multiplier by which the retry interval increases
        after each retry attempt.

        By default there is no backoff. Each retry will wait the amount of time
        specified by ``interval``.

        :default: 1 (no backoff)

        :stability: experimental
        '''
        result = self._values.get("backoff_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The interval (number of seconds) to wait between attempts.

        :default: Duration.seconds(5)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def total_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The total time that the state machine will wait for a successful response.

        :default: Duration.minutes(30)

        :stability: experimental
        '''
        result = self._values.get("total_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaiterStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApiCall)
class ApiCallBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/integ-tests-alpha.ApiCallBase",
):
    '''(experimental) Base class for an ApiCall.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5c30bd0d9d1e9f2d9b27538ad4782c94ca340a31438a5934b36cb27e41a106)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="assertAtPath")
    @abc.abstractmethod
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        Providing a path will filter the output of the initial API call.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="expect")
    def expect(self, expected: ExpectedResult) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall.

        :param expected: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7c9aa0f42f1a833762c8119488d08ffbe967de907a60b24f416cf7c564fd91)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(IApiCall, jsii.invoke(self, "expect", [expected]))

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _aws_cdk_ceddda9d.Reference:
        '''(experimental) Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cf0fe113d623960a2bcd5ecbfd05737f899bcc55e5ff0e8d2c5e1a4567ea46)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.invoke(self, "getAtt", [attribute_name]))

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''(experimental) Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880bbc28382f140bb446cd7a0a29b639affd6e2786540e3e1708003d74782721)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAttString", [attribute_name]))

    @jsii.member(jsii_name="next")
    def next(self, next: IApiCall) -> IApiCall:
        '''(experimental) Allows you to chain IApiCalls. This adds an explicit dependency betweent the two resources.

        Returns the IApiCall provided as ``next``

        :param next: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b474cc33c103ba8fec955b34c41238ccfcd11dbdb11f7e6a2438893d316b2afa)
            check_type(argname="argument next", value=next, expected_type=type_hints["next"])
        return typing.cast(IApiCall, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="waitForAssertions")
    @abc.abstractmethod
    def wait_for_assertions(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> IApiCall:
        '''(experimental) Wait for the IApiCall to return the expected response.

        If no expected response is specified then it will wait for
        the IApiCall to return a success

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="apiCallResource")
    @abc.abstractmethod
    def _api_call_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="provider")
    @abc.abstractmethod
    def provider(self) -> AssertionsProvider:
        '''(experimental) access the AssertionsProvider.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="flattenResponse")
    def _flatten_response(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "flattenResponse"))

    @_flatten_response.setter
    def _flatten_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97da9bf9b19a18aff40873ddc2b64a140954d8be0edcceff1c3ab02b28f3d0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flattenResponse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expectedResult")
    def _expected_result(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedResult"))

    @_expected_result.setter
    def _expected_result(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce4672396c2e9f40d0ddffe2d7e3f1a2da528acea1b0f4629b456ad9d0403be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputPaths")
    def _output_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputPaths"))

    @_output_paths.setter
    def _output_paths(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc878677ce52b96189eb1a58fb88ebee73b4b1bd3d713318ed57c1a58847f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def _state_machine_arn(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineArn"))

    @_state_machine_arn.setter
    def _state_machine_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f297ccd4c39b554ca2667c46f20d71a417fd6e796a8dc192158240ba2256123b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachineArn", value) # pyright: ignore[reportArgumentType]


class _ApiCallBaseProxy(ApiCallBase):
    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        Providing a path will filter the output of the initial API call.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13845f08ac36885e9e69aea7f533608f95aec490022e45da191534ce7c571fe8)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(IApiCall, jsii.invoke(self, "assertAtPath", [path, expected]))

    @jsii.member(jsii_name="waitForAssertions")
    def wait_for_assertions(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> IApiCall:
        '''(experimental) Wait for the IApiCall to return the expected response.

        If no expected response is specified then it will wait for
        the IApiCall to return a success

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        '''
        options = WaiterStateMachineOptions(
            backoff_rate=backoff_rate, interval=interval, total_timeout=total_timeout
        )

        return typing.cast(IApiCall, jsii.invoke(self, "waitForAssertions", [options]))

    @builtins.property
    @jsii.member(jsii_name="apiCallResource")
    def _api_call_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "apiCallResource"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> AssertionsProvider:
        '''(experimental) access the AssertionsProvider.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental
        '''
        return typing.cast(AssertionsProvider, jsii.get(self, "provider"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApiCallBase).__jsii_proxy_class__ = lambda : _ApiCallBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.AssertionsProviderProps",
    jsii_struct_bases=[LambdaFunctionProviderProps],
    name_mapping={
        "handler": "handler",
        "log_retention": "logRetention",
        "uuid": "uuid",
    },
)
class AssertionsProviderProps(LambdaFunctionProviderProps):
    def __init__(
        self,
        *,
        handler: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an AssertionsProvider.

        :param handler: (experimental) The handler to use for the lambda function. Default: index.handler
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified
        :param uuid: (experimental) This determines the uniqueness of each AssertionsProvider. You should only need to provide something different here if you *know* that you need a separate provider Default: - the default uuid is used

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.integ_tests_alpha as integ_tests_alpha
            from aws_cdk import aws_logs as logs
            
            assertions_provider_props = integ_tests_alpha.AssertionsProviderProps(
                handler="handler",
                log_retention=logs.RetentionDays.ONE_DAY,
                uuid="uuid"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5e060905b379d8af8619d5ea408511fba77814517c07abbda12acf1dbe165b)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if handler is not None:
            self._values["handler"] = handler
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''(experimental) The handler to use for the lambda function.

        :default: index.handler

        :stability: experimental
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) How long, in days, the log contents will be retained.

        :default: - no retention days specified

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''(experimental) This determines the uniqueness of each AssertionsProvider.

        You should only need to provide something different here if you
        *know* that you need a separate provider

        :default: - the default uuid is used

        :stability: experimental
        '''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionsProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsApiCall(
    ApiCallBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.AwsApiCall",
):
    '''(experimental) Construct that creates a custom resource that will perform a query using the AWS SDK.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # stack: Stack
        
        
        AwsApiCall(stack, "MyAssertion",
            service="SQS",
            api="receiveMessage",
            parameters={
                "QueueUrl": "url"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api: builtins.str,
        service: builtins.str,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api: (experimental) The api call to make, i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service, i.e. S3.
        :param output_paths: (experimental) Restrict the data returned by the API call to specific paths in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Default: - return all data
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e538fc4583813356d54f185265235ce446a780672975e15bbe5fa65cbba69a5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsApiCallProps(
            api=api, service=service, output_paths=output_paths, parameters=parameters
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        Providing a path will filter the output of the initial API call.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c820409bea110666051dd23cfad75a1450d07826755868229c2b4934ec0bad8)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(IApiCall, jsii.invoke(self, "assertAtPath", [path, expected]))

    @jsii.member(jsii_name="waitForAssertions")
    def wait_for_assertions(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> IApiCall:
        '''(experimental) Wait for the IApiCall to return the expected response.

        If no expected response is specified then it will wait for
        the IApiCall to return a success

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        '''
        options = WaiterStateMachineOptions(
            backoff_rate=backoff_rate, interval=interval, total_timeout=total_timeout
        )

        return typing.cast(IApiCall, jsii.invoke(self, "waitForAssertions", [options]))

    @builtins.property
    @jsii.member(jsii_name="apiCallResource")
    def _api_call_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "apiCallResource"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> AssertionsProvider:
        '''(experimental) access the AssertionsProvider.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental
        '''
        return typing.cast(AssertionsProvider, jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="waiterProvider")
    def waiter_provider(self) -> typing.Optional[AssertionsProvider]:
        '''(experimental) access the AssertionsProvider for the waiter state machine.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental

        Example::

            # api_call: AwsApiCall
            
            api_call.waiter_provider.add_to_role_policy({
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": ["*"]
            })
        '''
        return typing.cast(typing.Optional[AssertionsProvider], jsii.get(self, "waiterProvider"))

    @waiter_provider.setter
    def waiter_provider(self, value: typing.Optional[AssertionsProvider]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e978f2b80fc7ca4cf867ebf9e4673daf1582477274721902259a31caf906a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waiterProvider", value) # pyright: ignore[reportArgumentType]


class HttpApiCall(
    ApiCallBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.HttpApiCall",
):
    '''(experimental) Construct that creates a custom resource that will perform an HTTP API Call.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # stack: Stack
        
        
        HttpApiCall(stack, "MyAsssertion",
            url="https://example-api.com/abc"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        url: builtins.str,
        fetch_options: typing.Optional[typing.Union[FetchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param url: (experimental) The url to fetch.
        :param fetch_options: (experimental) Options for fetch.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0209121e751279aa416df5a16ee8548cf444948c1d390c4c88c07eb8c6b1c58a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpCallProps(url=url, fetch_options=fetch_options)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(
        self,
        _path: builtins.str,
        _expected: ExpectedResult,
    ) -> IApiCall:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        Providing a path will filter the output of the initial API call.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param _path: -
        :param _expected: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb5f6f39838f44a897965a4772b5b6db17ad826ce021bb98080a9af10f1207c9)
            check_type(argname="argument _path", value=_path, expected_type=type_hints["_path"])
            check_type(argname="argument _expected", value=_expected, expected_type=type_hints["_expected"])
        return typing.cast(IApiCall, jsii.invoke(self, "assertAtPath", [_path, _expected]))

    @jsii.member(jsii_name="waitForAssertions")
    def wait_for_assertions(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> IApiCall:
        '''(experimental) Wait for the IApiCall to return the expected response.

        If no expected response is specified then it will wait for
        the IApiCall to return a success

        :param backoff_rate: (experimental) Backoff between attempts. This is the multiplier by which the retry interval increases after each retry attempt. By default there is no backoff. Each retry will wait the amount of time specified by ``interval``. Default: 1 (no backoff)
        :param interval: (experimental) The interval (number of seconds) to wait between attempts. Default: Duration.seconds(5)
        :param total_timeout: (experimental) The total time that the state machine will wait for a successful response. Default: Duration.minutes(30)

        :stability: experimental
        '''
        options = WaiterStateMachineOptions(
            backoff_rate=backoff_rate, interval=interval, total_timeout=total_timeout
        )

        return typing.cast(IApiCall, jsii.invoke(self, "waitForAssertions", [options]))

    @builtins.property
    @jsii.member(jsii_name="apiCallResource")
    def _api_call_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "apiCallResource"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> AssertionsProvider:
        '''(experimental) access the AssertionsProvider.

        This can be used to add additional IAM policies
        the the provider role policy

        :stability: experimental
        '''
        return typing.cast(AssertionsProvider, jsii.get(self, "provider"))


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests-alpha.HttpCallProps",
    jsii_struct_bases=[HttpRequestParameters],
    name_mapping={"url": "url", "fetch_options": "fetchOptions"},
)
class HttpCallProps(HttpRequestParameters):
    def __init__(
        self,
        *,
        url: builtins.str,
        fetch_options: typing.Optional[typing.Union[FetchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for creating an HttpApiCall provider.

        :param url: (experimental) The url to fetch.
        :param fetch_options: (experimental) Options for fetch.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # stack: Stack
            
            
            HttpApiCall(stack, "MyAsssertion",
                url="https://example-api.com/abc"
            )
        '''
        if isinstance(fetch_options, dict):
            fetch_options = FetchOptions(**fetch_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4a71f13aa64d1306c572e9f98559d007cead2ee1c483183f46e1dad96274fd)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument fetch_options", value=fetch_options, expected_type=type_hints["fetch_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if fetch_options is not None:
            self._values["fetch_options"] = fetch_options

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The url to fetch.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fetch_options(self) -> typing.Optional[FetchOptions]:
        '''(experimental) Options for fetch.

        :stability: experimental
        '''
        result = self._values.get("fetch_options")
        return typing.cast(typing.Optional[FetchOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpCallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaInvokeFunction(
    AwsApiCall,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests-alpha.LambdaInvokeFunction",
):
    '''(experimental) An AWS Lambda Invoke function API call.

    Use this instead of the generic AwsApiCall in order to
    invoke a lambda function. This will automatically create
    the correct permissions to invoke the function

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.integ_tests_alpha as integ_tests_alpha
        from aws_cdk import aws_logs as logs
        
        lambda_invoke_function = integ_tests_alpha.LambdaInvokeFunction(self, "MyLambdaInvokeFunction",
            function_name="functionName",
        
            # the properties below are optional
            invocation_type=integ_tests_alpha.InvocationType.EVENT,
            log_retention=logs.RetentionDays.ONE_DAY,
            log_type=integ_tests_alpha.LogType.NONE,
            payload="payload"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional[InvocationType] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_type: typing.Optional[LogType] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONSE
        :param log_retention: (experimental) How long, in days, the log contents will be retained. Default: - no retention days specified
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc846004ad65c16a9a1322c4c518ae25ebd02b2bc7803230f5bb11a2884f1de0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaInvokeFunctionProps(
            function_name=function_name,
            invocation_type=invocation_type,
            log_retention=log_retention,
            log_type=log_type,
            payload=payload,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "ActualResult",
    "ApiCallBase",
    "AssertionRequest",
    "AssertionResult",
    "AssertionResultData",
    "AssertionType",
    "AssertionsProvider",
    "AssertionsProviderProps",
    "AwsApiCall",
    "AwsApiCallOptions",
    "AwsApiCallProps",
    "AwsApiCallRequest",
    "AwsApiCallResult",
    "EqualsAssertion",
    "EqualsAssertionProps",
    "ExpectedResult",
    "FetchOptions",
    "HttpApiCall",
    "HttpCallProps",
    "HttpRequest",
    "HttpRequestParameters",
    "HttpResponse",
    "HttpResponseWrapper",
    "IApiCall",
    "IDeployAssert",
    "IntegTest",
    "IntegTestCase",
    "IntegTestCaseProps",
    "IntegTestCaseStack",
    "IntegTestCaseStackProps",
    "IntegTestProps",
    "InvocationType",
    "LambdaFunctionProviderProps",
    "LambdaInvokeFunction",
    "LambdaInvokeFunctionProps",
    "LogType",
    "Match",
    "Status",
    "WaiterStateMachine",
    "WaiterStateMachineOptions",
    "WaiterStateMachineProps",
]

publication.publish()

def _typecheckingstub__db8960192c69b2034028024915394db8e014653a8888980859f2e3547a455daa(
    query: IApiCall,
    attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927c94a66cbe073d89039c4e27e1104a29d36865645ee1ba163e752be4da99a6(
    custom_resource: _aws_cdk_ceddda9d.CustomResource,
    attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0def0e46807bcce5f5541c6cce0db0cd558065170e086f1248e1fbff32e95abd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775e367a8b9b90eff85fd16c452c0ee84b1903d6aef4bbeec51fb738c386310b(
    *,
    actual: typing.Any,
    expected: typing.Any,
    fail_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75fa6e1a3201fe0fa6cf710bf3ea3f500448d16b191232e4e335385d56e566e(
    *,
    assertion: builtins.str,
    failed: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebef927d19dce3506807a648e225e27c5cee3900a2c2693bc29ecaad2d38101(
    *,
    status: Status,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d829d3346bf088cede720be581add7c49c5142d6b67835d095d5b7fc2f3be071(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    uuid: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285397c0e0cbfc08b4ceb96a2add1fa4e5526f2b30516e8392967f5137179e44(
    service: builtins.str,
    api: builtins.str,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce43eeb4052a2bec14220d62d9e29dabfd6cd994cea93852c4eeea7119d694e(
    statement: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aead2da0479681240000a232baddbe9a576e79f1bb8c553c4fc2eb15334792c(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15205a41c415f7c6befb41d2657e281256b15aca69cb25c1fe72c1803a5e34f8(
    principal_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb3bfb6e039f1770b7357b50e700e5397b1fe0af7e9bda38fcf799b232ae6b1(
    *,
    api: builtins.str,
    service: builtins.str,
    output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9667093e2c183b6409c654dfeddf1ba9117d05548446571b59e368fb53b52357(
    *,
    api: builtins.str,
    service: builtins.str,
    output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c5b4f02fb0af656efa41ad3e0b46bca31caf2520a4a6f541428609610641b2(
    *,
    api: builtins.str,
    service: builtins.str,
    flatten_response: typing.Optional[builtins.str] = None,
    output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e3f1f73e49e1577977c7911e8cc8c5ef685546bdc133fdea8e9544cb4fd96b(
    *,
    api_call_response: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c04e443c11a2367321899a4898db5e5d6620d46b9e0d1b3fa31d7e9dd021554(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    actual: ActualResult,
    expected: ExpectedResult,
    fail_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58af14cdbf1ae6af7373273fada4bab47f80572e2dc79fc8406588336d4cd06a(
    *,
    actual: ActualResult,
    expected: ExpectedResult,
    fail_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f650c234de69311d3be1555c76c31b0bcf660ee568cb8877337aaa3fcc56a59(
    expected: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba1bd6868bcbf917d8781a68e462486356d1b72f71281beafa06866afb05e73(
    expected: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41760596828a67f336d3d40b1a2fade70ac97e61371e5de90c1ba47717728f61(
    expected: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba074a7cbb4cb81e3710d0722f59a4ad232869166467c789883b0d1ea35bf92(
    expected: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33010e7c2f43ad7b078d998ca478ef09e6cf76bc2eadeb12407d48e7f8d56d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e88c6f6439b0e809ba451cf7d5fdcb3370b99a16f4d97c6d1c6ff524a91f56(
    *,
    body: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    method: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e43070ab7c42531f81da281a2f078d3aaa5c2747ce7ed529dd5083e0ecf1f15(
    *,
    parameters: typing.Union[HttpRequestParameters, typing.Dict[builtins.str, typing.Any]],
    flatten_response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93af9c54916c56a6f8f854ed0b3f9f13208556a5bdfc783196525c8d6ac46dab(
    *,
    url: builtins.str,
    fetch_options: typing.Optional[typing.Union[FetchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391c496ab114dbafa2050e50cd71e9603e3723e49e2d262950bd96589530e06a(
    *,
    body: typing.Any = None,
    headers: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ok: typing.Optional[builtins.bool] = None,
    status: typing.Optional[jsii.Number] = None,
    status_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa97df0d1c119f8060810ef7873d7cbafff7b4b83e883dff6b5be3ec2fbbd17b(
    *,
    api_call_response: typing.Union[HttpResponse, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f411c9c6ce09258efafb36af27db400c2f261d107ee630843a9353825628ab2a(
    path: builtins.str,
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddf80736a88c6c822d6a25fbc32b7351e8da3accd460b8d16ff71eb55de6046(
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfacb64b65fabe2392dc2b549890ca1c6de3d73472d8f4bbf082087228f4a805(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecdf8894538ec23be7a00dac9133f608b80e8936665f4e1662ec5277f92ee17(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bcab731afdde04f06b7b02cad97732570960e944e237d4caa43e6fbceaf938(
    next: IApiCall,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0016b9ee68480906b65c3f2abda1a5eef570a527959ef608ac4d86836e7f4b28(
    service: builtins.str,
    api: builtins.str,
    parameters: typing.Any = None,
    output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5691b1933125f6e27b8109881a6206c07bcdea66d6a2a61d313cd6f7b30ce8(
    id: builtins.str,
    expected: ExpectedResult,
    actual: ActualResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9053497bae85d950ab08f20afee06c8e7c3e89c63f987e0320dba88e432ddff5(
    url: builtins.str,
    *,
    body: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    method: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fb8761c88b4fc9579f6a32db4edfe539963bdb489338e7e428d98f41281684(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    test_cases: typing.Sequence[_aws_cdk_ceddda9d.Stack],
    assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
    enable_lookups: typing.Optional[builtins.bool] = None,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93909b22bdb434dd5bf6d9361625228bbeaf85254c3fc7bc9e72b77b70fd0e1f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stacks: typing.Sequence[_aws_cdk_ceddda9d.Stack],
    assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f36706ce503fa92c9baffb37b25208bc4e61071c2af78b1cf526c1916f483b6(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    stacks: typing.Sequence[_aws_cdk_ceddda9d.Stack],
    assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3a10010962bdab5e34756e8b8781def4d66140bc39b762ac839b6431134b6e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    property_injectors: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPropertyInjector]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0f2ea15e16068a7686e303272abe9b66aff6f74e31067127bd671e0b6dfd1a(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59edf2938a92df2253021d942b03a0fa818705ff3df6920854079be734c3e175(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    property_injectors: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPropertyInjector]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2013546a0269b479331ed4cdfd706a8b20bf18d5f45e074d56ae77eb9b6dd4(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_cloud_assembly_schema_ceddda9d.Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    test_cases: typing.Sequence[_aws_cdk_ceddda9d.Stack],
    assertion_stack: typing.Optional[_aws_cdk_ceddda9d.Stack] = None,
    enable_lookups: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38d440a6e46009e1964a16dca6cca6a65cee4a96c1e4ec4505f3cc068bc45c1(
    *,
    handler: typing.Optional[builtins.str] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f94aeefe8016f3f35355f86e35cc34b53e597152be16a8b6a678afab636d7b(
    *,
    function_name: builtins.str,
    invocation_type: typing.Optional[InvocationType] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_type: typing.Optional[LogType] = None,
    payload: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cd8dd33ba371f84a9b655b09b12aca9fda33749b1d492e04e29de74e17ce19(
    pattern: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ed9ce4ac8ba15c74fcb4d77253ca710ec1f313d1f47ebb3641222f363fc260(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6f20a7536a39c152b01944858b6ec7920308d8ab4b26ce4ca075855f0c4aae(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b86e0fb528b0809c81fd8c9509acd452ec22cd078f57824f27506c9ac85d9b(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99521e6ae1132d620337d92d0e6db2d69a603a34b4b8ff711ffc16a33f710a3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    backoff_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121fca5df71218eb18c08109872208325ee23307067d82bcba84288b6feccd22(
    *,
    backoff_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e828ea92e322e9108a7c287fff81908fdb3933543431b12a3a1c1252a39520e(
    *,
    backoff_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5c30bd0d9d1e9f2d9b27538ad4782c94ca340a31438a5934b36cb27e41a106(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7c9aa0f42f1a833762c8119488d08ffbe967de907a60b24f416cf7c564fd91(
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cf0fe113d623960a2bcd5ecbfd05737f899bcc55e5ff0e8d2c5e1a4567ea46(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880bbc28382f140bb446cd7a0a29b639affd6e2786540e3e1708003d74782721(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b474cc33c103ba8fec955b34c41238ccfcd11dbdb11f7e6a2438893d316b2afa(
    next: IApiCall,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97da9bf9b19a18aff40873ddc2b64a140954d8be0edcceff1c3ab02b28f3d0c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce4672396c2e9f40d0ddffe2d7e3f1a2da528acea1b0f4629b456ad9d0403be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc878677ce52b96189eb1a58fb88ebee73b4b1bd3d713318ed57c1a58847f30(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f297ccd4c39b554ca2667c46f20d71a417fd6e796a8dc192158240ba2256123b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13845f08ac36885e9e69aea7f533608f95aec490022e45da191534ce7c571fe8(
    path: builtins.str,
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5e060905b379d8af8619d5ea408511fba77814517c07abbda12acf1dbe165b(
    *,
    handler: typing.Optional[builtins.str] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e538fc4583813356d54f185265235ce446a780672975e15bbe5fa65cbba69a5b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api: builtins.str,
    service: builtins.str,
    output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c820409bea110666051dd23cfad75a1450d07826755868229c2b4934ec0bad8(
    path: builtins.str,
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e978f2b80fc7ca4cf867ebf9e4673daf1582477274721902259a31caf906a43(
    value: typing.Optional[AssertionsProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0209121e751279aa416df5a16ee8548cf444948c1d390c4c88c07eb8c6b1c58a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    url: builtins.str,
    fetch_options: typing.Optional[typing.Union[FetchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5f6f39838f44a897965a4772b5b6db17ad826ce021bb98080a9af10f1207c9(
    _path: builtins.str,
    _expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4a71f13aa64d1306c572e9f98559d007cead2ee1c483183f46e1dad96274fd(
    *,
    url: builtins.str,
    fetch_options: typing.Optional[typing.Union[FetchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc846004ad65c16a9a1322c4c518ae25ebd02b2bc7803230f5bb11a2884f1de0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    function_name: builtins.str,
    invocation_type: typing.Optional[InvocationType] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_type: typing.Optional[LogType] = None,
    payload: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
