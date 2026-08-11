r'''
# AWS::States Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_states as states
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for States construct libraries](https://constructs.dev/search?q=states)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::States resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_States.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::States](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_States.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
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


from .._jsii import *

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
    import aws_cdk.interfaces.aws_states as _aws_states_fbd6b6e3
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_states_fbd6b6e3 = _LazyImport("aws_cdk.interfaces.aws_states")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_states_fbd6b6e3.IExecutionRef)
class CfnExecution(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_states.CfnExecution",
):
    '''Represents an AWS Step Functions state machine execution.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-states-execution.html
    :cloudformationResource: AWS::States::Execution
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_states as states
        
        cfn_execution = states.CfnExecution(self, "MyCfnExecution",
            state_machine_arn="stateMachineArn",
        
            # the properties below are optional
            input="input",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        state_machine_arn: builtins.str,
        input: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::States::Execution``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param state_machine_arn: The Amazon Resource Name (ARN) of the state machine that was executed.
        :param input: The string that contains the JSON input data for the execution.
        :param name: The name of the execution.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ecaf1275843938b9fa9af6ca1612f7670bcd8ca0e8448a7e617f281a4cf11e30)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnExecutionProps(
            state_machine_arn=state_machine_arn, input=input, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForExecution")
    @builtins.classmethod
    def arn_for_execution(
        cls,
        resource: "_aws_states_fbd6b6e3.IExecutionRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ce0ac973751edde198701b57155132d848104425f250453da87405f64c5c0024)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForExecution", [resource]))

    @jsii.member(jsii_name="isCfnExecution")
    @builtins.classmethod
    def is_cfn_execution(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnExecution.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9b98aa9c479f54b121a379d1c3cdd6c92686fcfd409b94efe7cb684ea29c16e7)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnExecution", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c61cc2a8d379990c171c363e8097aa9fe29ba7877631b7ebbd4383e40a44b28c)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f5d59c0d71590aa0bb8a2425878eb3b7e45f7b7c3fe8eb60947277146c1a84b4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrExecutionArn")
    def attr_execution_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) that identifies the execution.

        :cloudformationAttribute: ExecutionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrExecutionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRedriveCount")
    def attr_redrive_count(self) -> jsii.Number:
        '''The number of times the execution has been redriven.

        :cloudformationAttribute: RedriveCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRedriveCount"))

    @builtins.property
    @jsii.member(jsii_name="attrRedriveStatus")
    def attr_redrive_status(self) -> builtins.str:
        '''Indicates whether or not an execution can be redriven.

        :cloudformationAttribute: RedriveStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRedriveStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStartDate")
    def attr_start_date(self) -> builtins.str:
        '''The date the execution started.

        :cloudformationAttribute: StartDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStartDate"))

    @builtins.property
    @jsii.member(jsii_name="attrStateMachineName")
    def attr_state_machine_name(self) -> builtins.str:
        '''The name of the state machine, extracted from the execution ARN.

        :cloudformationAttribute: StateMachineName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStateMachineName"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the execution.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="executionRef")
    def execution_ref(self) -> "_aws_states_fbd6b6e3.ExecutionReference":
        '''A reference to a Execution resource.'''
        return typing.cast("_aws_states_fbd6b6e3.ExecutionReference", jsii.get(self, "executionRef"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the state machine that was executed.'''
        return typing.cast(builtins.str, jsii.get(self, "stateMachineArn"))

    @state_machine_arn.setter
    def state_machine_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3ed5e2e4cf70263b2fc0d4d4282aba2cd4b00ccbc84547badd0424116c74d4a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachineArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> typing.Optional[builtins.str]:
        '''The string that contains the JSON input data for the execution.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "input"))

    @input.setter
    def input(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0361459949fbb07cb0c4e95d02616cc2640497a9d7ab657e0cfd7824d2f6021c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "input", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the execution.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5da8cfc0bbeec72b1efb3b6f916ad32e1f42b71aac75306708cece248e893e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_states.CfnExecutionProps",
    jsii_struct_bases=[],
    name_mapping={
        "state_machine_arn": "stateMachineArn",
        "input": "input",
        "name": "name",
    },
)
class CfnExecutionProps:
    def __init__(
        self,
        *,
        state_machine_arn: builtins.str,
        input: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnExecution``.

        :param state_machine_arn: The Amazon Resource Name (ARN) of the state machine that was executed.
        :param input: The string that contains the JSON input data for the execution.
        :param name: The name of the execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-states-execution.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_states as states
            
            cfn_execution_props = states.CfnExecutionProps(
                state_machine_arn="stateMachineArn",
            
                # the properties below are optional
                input="input",
                name="name"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3228b6aa8d7e48030775f40c91f33e0f4f3394be5d7bdb51d9ad66ac43821ea8)
            check_type(argname="argument state_machine_arn", value=state_machine_arn, expected_type=type_hints["state_machine_arn"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state_machine_arn": state_machine_arn,
        }
        if input is not None:
            self._values["input"] = input
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def state_machine_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the state machine that was executed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-states-execution.html#cfn-states-execution-statemachinearn
        '''
        result = self._values.get("state_machine_arn")
        assert result is not None, "Required property 'state_machine_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input(self) -> typing.Optional[builtins.str]:
        '''The string that contains the JSON input data for the execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-states-execution.html#cfn-states-execution-input
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-states-execution.html#cfn-states-execution-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnExecution",
    "CfnExecutionProps",
]

publication.publish()

def _typecheckingstub__ecaf1275843938b9fa9af6ca1612f7670bcd8ca0e8448a7e617f281a4cf11e30(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    state_machine_arn: builtins.str,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0ac973751edde198701b57155132d848104425f250453da87405f64c5c0024(
    resource: _aws_states_fbd6b6e3.IExecutionRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b98aa9c479f54b121a379d1c3cdd6c92686fcfd409b94efe7cb684ea29c16e7(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61cc2a8d379990c171c363e8097aa9fe29ba7877631b7ebbd4383e40a44b28c(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d59c0d71590aa0bb8a2425878eb3b7e45f7b7c3fe8eb60947277146c1a84b4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed5e2e4cf70263b2fc0d4d4282aba2cd4b00ccbc84547badd0424116c74d4a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0361459949fbb07cb0c4e95d02616cc2640497a9d7ab657e0cfd7824d2f6021c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da8cfc0bbeec72b1efb3b6f916ad32e1f42b71aac75306708cece248e893e88(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3228b6aa8d7e48030775f40c91f33e0f4f3394be5d7bdb51d9ad66ac43821ea8(
    *,
    state_machine_arn: builtins.str,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
