r'''
# `cdk-secret-manager-wrapper-layer`

that Lambda layer uses a wrapper script to fetch information from Secrets Manager and create environmental variables.

> idea from [source](https://github.com/aws-samples/aws-lambda-environmental-variables-from-aws-secrets-manager)

## Updates

**2025-03-02: v2.1.0**

* Added architecture parameter support for Lambda Layer
* Updated Python runtime from 3.9 to 3.13
* Fixed handler name in example code
* Improved layer initialization and referencing patterns
* Enhanced compatibility with AWS Lambda ARM64 architecture

## Example

```python
import { App, Stack, CfnOutput, Duration } from 'aws-cdk-lib';
import { Effect, PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Function, Runtime, Code, FunctionUrlAuthType, Architecture } from 'aws-cdk-lib/aws-lambda';
import { CfnSecret } from 'aws-cdk-lib/aws-secretsmanager';
import { SecretManagerWrapperLayer } from 'cdk-secret-manager-wrapper-layer';
const env = {
  region: process.env.CDK_DEFAULT_REGION,
  account: process.env.CDK_DEFAULT_ACCOUNT,
};
const app = new App();
const stack = new Stack(app, 'testing-stack', { env });

/**
 * Example create an Secret for testing.
 */
const secret = new CfnSecret(stack, 'MySecret', {
  secretString: JSON.stringify({
    KEY1: 'VALUE1',
    KEY2: 'VALUE2',
    KEY3: 'VALUE3',
  }),
});

const lambdaArchitecture = Architecture.X86_64;

const layer = new SecretManagerWrapperLayer(stack, 'SecretManagerWrapperLayer', {
  lambdaArchitecture,
});

const lambda = new Function(stack, 'fn', {
  runtime: Runtime.PYTHON_3_13,
  code: Code.fromInline(`
import os
def handler(events, contexts):
    env = {}
    env['KEY1'] = os.environ.get('KEY1', 'Not Found')
    env['KEY2'] = os.environ.get('KEY2', 'Not Found')
    env['KEY3'] = os.environ.get('KEY3', 'Not Found')
    return env
    `),
  handler: 'index.handler',
  layers: [layer.layerVersion],
  timeout: Duration.minutes(1),
  /**
   * you need to define this 4 environment various.
   */
  environment: {
    AWS_LAMBDA_EXEC_WRAPPER: '/opt/get-secrets-layer',
    SECRET_REGION: stack.region,
    SECRET_ARN: secret.ref,
    API_TIMEOUT: '5000',
  },
  architecture: lambdaArchitecture,
});

/**
 * Add Permission for lambda get secret value from secret manager.
 */
lambda.role!.addToPrincipalPolicy(
  new PolicyStatement({
    effect: Effect.ALLOW,
    actions: ['secretsmanager:GetSecretValue'],
    // Also you can use find from context.
    resources: [secret.ref],
  }),
);

/**
 * For Testing.
 */
const FnUrl = lambda.addFunctionUrl({
  authType: FunctionUrlAuthType.NONE,
});

new CfnOutput(stack, 'FnUrl', {
  value: FnUrl.url,
});
```

## Testing

```bash
# ex: curl https://sdfghjklertyuioxcvbnmghj.lambda-url.us-east-1.on.aws/
curl ${FnUrl}
{"KEY2":"VALUE2","KEY1":"VALUE1","KEY3":"VALUE3"}
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

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class SecretManagerWrapperLayer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-secret-manager-wrapper-layer.SecretManagerWrapperLayer",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_architecture: (experimental) The architecture for the Lambda function that will use this layer.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ffb39aa2a0e2e2a32a6428a50af4da3ab83165cae954863332d289d007447bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretManagerWrapperLayerProps(lambda_architecture=lambda_architecture)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="layerVersion")
    def layer_version(self) -> _aws_cdk_aws_lambda_ceddda9d.ILayerVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.ILayerVersion, jsii.get(self, "layerVersion"))


@jsii.data_type(
    jsii_type="cdk-secret-manager-wrapper-layer.SecretManagerWrapperLayerProps",
    jsii_struct_bases=[],
    name_mapping={"lambda_architecture": "lambdaArchitecture"},
)
class SecretManagerWrapperLayerProps:
    def __init__(
        self,
        *,
        lambda_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    ) -> None:
        '''
        :param lambda_architecture: (experimental) The architecture for the Lambda function that will use this layer.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524b68bc4f6f4ba7515f1e15f1ce7839f9063fa179a96dced4c022f91447f7e9)
            check_type(argname="argument lambda_architecture", value=lambda_architecture, expected_type=type_hints["lambda_architecture"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lambda_architecture is not None:
            self._values["lambda_architecture"] = lambda_architecture

    @builtins.property
    def lambda_architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''(experimental) The architecture for the Lambda function that will use this layer.

        :stability: experimental
        '''
        result = self._values.get("lambda_architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerWrapperLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecretManagerWrapperLayer",
    "SecretManagerWrapperLayerProps",
]

publication.publish()

def _typecheckingstub__5ffb39aa2a0e2e2a32a6428a50af4da3ab83165cae954863332d289d007447bd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524b68bc4f6f4ba7515f1e15f1ce7839f9063fa179a96dced4c022f91447f7e9(
    *,
    lambda_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
) -> None:
    """Type checking stubs"""
    pass
