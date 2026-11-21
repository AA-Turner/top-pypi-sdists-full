from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from ..._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk as _aws_cdk_0cae9daa
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


class FunctionRuntimeConfig(
    _aws_cdk_0cae9daa.Mixin,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_lambda.mixins.FunctionRuntimeConfig",
):
    '''Lambda-specific Mixin to run a function on a customer-managed runtime (CMR).

    Sets the ``runtimeConfig`` property on the function, replacing any existing
    ``runtimeConfig``. The function's runtime must be ``custom``, and the function
    must not be a container image function; both are checked at synthesis, so a
    runtime or package type set after the mixin is applied is still checked. A
    runtime that is only known at deployment, such as a parameter value, is not
    checked.

    Which runtime versions and architectures the runtime supports, and whether
    the calling account may use it, are validated by the service at deployment.

    :exampleMetadata: infused

    Example::

        lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime("custom", lambda_.RuntimeFamily.OTHER),
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
        ).with(lambda_.mixins.FunctionRuntimeConfig(
            runtime_arn="arn:aws:lambda:us-east-1:123456789012:runtime/my-python-runtime",
            runtime_alias="stable"
        ))
    '''

    def __init__(
        self,
        *,
        runtime_alias: builtins.str,
        runtime_arn: builtins.str,
    ) -> None:
        '''
        :param runtime_alias: The name of the runtime alias that selects which runtime version the function runs on (for example ``stable`` or ``latest``). With the default ``RuntimeManagementMode.AUTO``, moving the alias to a new version rolls the function forward on its next cold start, without a function redeploy.
        :param runtime_arn: The ARN of the customer-managed runtime that the function uses, for example ``arn:aws:lambda:us-east-1:123456789012:runtime/my-runtime``. The specific runtime version is resolved by the service from ``runtimeAlias``.
        '''
        props = FunctionRuntimeConfigProps(
            runtime_alias=runtime_alias, runtime_arn=runtime_arn
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="applyTo")
    def apply_to(self, construct: "_constructs_77d1e7e8.IConstruct") -> None:
        '''Applies the mixin functionality to the target construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ec3c211a645fff6fbb51f314f3d44b032e279cd33beb6f35845cb4c707d10416)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(None, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: "_constructs_77d1e7e8.IConstruct") -> builtins.bool:
        '''Determines whether this mixin can be applied to the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e12dc199e8dacc0c05e9f270e73f9f621f6cb4ad7b604f3d785d9938f578ef22)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_lambda.mixins.FunctionRuntimeConfigProps",
    jsii_struct_bases=[],
    name_mapping={"runtime_alias": "runtimeAlias", "runtime_arn": "runtimeArn"},
)
class FunctionRuntimeConfigProps:
    def __init__(
        self,
        *,
        runtime_alias: builtins.str,
        runtime_arn: builtins.str,
    ) -> None:
        '''Properties for the FunctionRuntimeConfig mixin.

        :param runtime_alias: The name of the runtime alias that selects which runtime version the function runs on (for example ``stable`` or ``latest``). With the default ``RuntimeManagementMode.AUTO``, moving the alias to a new version rolls the function forward on its next cold start, without a function redeploy.
        :param runtime_arn: The ARN of the customer-managed runtime that the function uses, for example ``arn:aws:lambda:us-east-1:123456789012:runtime/my-runtime``. The specific runtime version is resolved by the service from ``runtimeAlias``.

        :exampleMetadata: infused

        Example::

            lambda_.Function(self, "MyFunction",
                runtime=lambda_.Runtime("custom", lambda_.RuntimeFamily.OTHER),
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
            ).with(lambda_.mixins.FunctionRuntimeConfig(
                runtime_arn="arn:aws:lambda:us-east-1:123456789012:runtime/my-python-runtime",
                runtime_alias="stable"
            ))
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4bbb76030bae1ed36b47ede4b4a163bd714594254f0e8cf003e371b422286c42)
            check_type(argname="argument runtime_alias", value=runtime_alias, expected_type=type_hints["runtime_alias"])
            check_type(argname="argument runtime_arn", value=runtime_arn, expected_type=type_hints["runtime_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime_alias": runtime_alias,
            "runtime_arn": runtime_arn,
        }

    @builtins.property
    def runtime_alias(self) -> builtins.str:
        '''The name of the runtime alias that selects which runtime version the function runs on (for example ``stable`` or ``latest``).

        With the default ``RuntimeManagementMode.AUTO``, moving the alias to a new
        version rolls the function forward on its next cold start, without a
        function redeploy.
        '''
        result = self._values.get("runtime_alias")
        assert result is not None, "Required property 'runtime_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_arn(self) -> builtins.str:
        '''The ARN of the customer-managed runtime that the function uses, for example ``arn:aws:lambda:us-east-1:123456789012:runtime/my-runtime``.

        The specific runtime version is resolved by the service from ``runtimeAlias``.
        '''
        result = self._values.get("runtime_arn")
        assert result is not None, "Required property 'runtime_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionRuntimeConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FunctionRuntimeConfig",
    "FunctionRuntimeConfigProps",
]

publication.publish()

def _typecheckingstub__ec3c211a645fff6fbb51f314f3d44b032e279cd33beb6f35845cb4c707d10416(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12dc199e8dacc0c05e9f270e73f9f621f6cb4ad7b604f3d785d9938f578ef22(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbb76030bae1ed36b47ede4b4a163bd714594254f0e8cf003e371b422286c42(
    *,
    runtime_alias: builtins.str,
    runtime_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
