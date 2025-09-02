r'''
Documentation for this pattern can be found [here](https://github.com/awslabs/aws-solutions-constructs/blob/main/source/patterns/%40aws-solutions-constructs/aws-eventbridge-lambda/README.adoc)
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

import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class EventbridgeToLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-eventbridge-lambda.EventbridgeToLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
        event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
        existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
        lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param event_bus_props: A new custom EventBus is created with provided props. Default: - None
        :param existing_event_bus_interface: Existing instance of a custom EventBus. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object, providing both this and ``lambdaFunctionProps`` will cause an error. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used

        :access: public
        :summary: Constructs a new instance of the EventbridgeToLambda class.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30e2e323a73bab4ca7615824f49e27d237145681d48c68c596e038ae88a39ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EventbridgeToLambdaProps(
            event_rule_props=event_rule_props,
            event_bus_props=event_bus_props,
            existing_event_bus_interface=existing_event_bus_interface,
            existing_lambda_obj=existing_lambda_obj,
            lambda_function_props=lambda_function_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> _aws_cdk_aws_events_ceddda9d.Rule:
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.get(self, "eventsRule"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], jsii.get(self, "eventBus"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-eventbridge-lambda.EventbridgeToLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_rule_props": "eventRuleProps",
        "event_bus_props": "eventBusProps",
        "existing_event_bus_interface": "existingEventBusInterface",
        "existing_lambda_obj": "existingLambdaObj",
        "lambda_function_props": "lambdaFunctionProps",
    },
)
class EventbridgeToLambdaProps:
    def __init__(
        self,
        *,
        event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
        event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
        existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
        lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param event_bus_props: A new custom EventBus is created with provided props. Default: - None
        :param existing_event_bus_interface: Existing instance of a custom EventBus. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object, providing both this and ``lambdaFunctionProps`` will cause an error. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used

        :summary: The properties for the CloudFrontToApiGateway Construct
        '''
        if isinstance(event_rule_props, dict):
            event_rule_props = _aws_cdk_aws_events_ceddda9d.RuleProps(**event_rule_props)
        if isinstance(event_bus_props, dict):
            event_bus_props = _aws_cdk_aws_events_ceddda9d.EventBusProps(**event_bus_props)
        if isinstance(lambda_function_props, dict):
            lambda_function_props = _aws_cdk_aws_lambda_ceddda9d.FunctionProps(**lambda_function_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee206692daeaec69a69e4e43faf3b57a0df89a5e348545ee0b380b34931ab8a)
            check_type(argname="argument event_rule_props", value=event_rule_props, expected_type=type_hints["event_rule_props"])
            check_type(argname="argument event_bus_props", value=event_bus_props, expected_type=type_hints["event_bus_props"])
            check_type(argname="argument existing_event_bus_interface", value=existing_event_bus_interface, expected_type=type_hints["existing_event_bus_interface"])
            check_type(argname="argument existing_lambda_obj", value=existing_lambda_obj, expected_type=type_hints["existing_lambda_obj"])
            check_type(argname="argument lambda_function_props", value=lambda_function_props, expected_type=type_hints["lambda_function_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_rule_props": event_rule_props,
        }
        if event_bus_props is not None:
            self._values["event_bus_props"] = event_bus_props
        if existing_event_bus_interface is not None:
            self._values["existing_event_bus_interface"] = existing_event_bus_interface
        if existing_lambda_obj is not None:
            self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None:
            self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def event_rule_props(self) -> _aws_cdk_aws_events_ceddda9d.RuleProps:
        '''User provided eventRuleProps to override the defaults.

        :default: - None
        '''
        result = self._values.get("event_rule_props")
        assert result is not None, "Required property 'event_rule_props' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.RuleProps, result)

    @builtins.property
    def event_bus_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.EventBusProps]:
        '''A new custom EventBus is created with provided props.

        :default: - None
        '''
        result = self._values.get("event_bus_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.EventBusProps], result)

    @builtins.property
    def existing_event_bus_interface(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        '''Existing instance of a custom EventBus.

        :default: - None
        '''
        result = self._values.get("existing_event_bus_interface")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], result)

    @builtins.property
    def existing_lambda_obj(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function]:
        '''Existing instance of Lambda Function object, providing both this and ``lambdaFunctionProps`` will cause an error.

        :default: - None
        '''
        result = self._values.get("existing_lambda_obj")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function], result)

    @builtins.property
    def lambda_function_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionProps]:
        '''User provided props to override the default props for the Lambda function.

        :default: - Default props are used
        '''
        result = self._values.get("lambda_function_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventbridgeToLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventbridgeToLambda",
    "EventbridgeToLambdaProps",
]

publication.publish()

def _typecheckingstub__f30e2e323a73bab4ca7615824f49e27d237145681d48c68c596e038ae88a39ce(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
    event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
    lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee206692daeaec69a69e4e43faf3b57a0df89a5e348545ee0b380b34931ab8a(
    *,
    event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
    event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
    lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
